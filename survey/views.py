import json
import re

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .ai import model as ai_model
from .forms import FieldForm, FormCreateForm, SignupForm
from .models import Answer, Field, Form, Response

PHONE_RE = re.compile(r"^[\d+\-\s()]{6,20}$")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME_RE = re.compile(r"^\d{2}:\d{2}(:\d{2})?$")


def _cors(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type"
    return response


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "survey/home.html")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignupForm()
    return render(request, "survey/signup.html", {"form": form})


@login_required
def dashboard(request):
    forms = Form.objects.filter(owner=request.user)
    return render(request, "survey/dashboard.html", {"forms": forms})


@login_required
def form_create(request):
    if request.method == "POST":
        form = FormCreateForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.owner = request.user
            new_form.save()
            return redirect("form-detail", slug=new_form.slug)
    else:
        form = FormCreateForm()
    return render(request, "survey/form_create.html", {"form": form})


@login_required
@require_http_methods(["POST"])
def ai_suggest(request):
    """Return a JSON suggestion (title, description, fields) for a purpose."""
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    purpose = (data.get("purpose") or "").strip()
    if not purpose:
        return JsonResponse({"error": "Please describe your form's purpose."}, status=400)
    if len(purpose) > 500:
        return JsonResponse({"error": "Description is too long (max 500 characters)."}, status=400)
    suggestion = ai_model.suggest(purpose)
    if suggestion is None:
        return JsonResponse({"error": "Could not generate a suggestion."}, status=400)
    return JsonResponse(suggestion)


@login_required
@require_http_methods(["POST"])
def ai_apply(request):
    """Create a new form from an AI suggestion (server-side; ignores client edits to fields)."""
    purpose = (request.POST.get("purpose") or "").strip()
    title = (request.POST.get("title") or "").strip()
    description = (request.POST.get("description") or "").strip()
    if not purpose or not title:
        return redirect("form-create")
    suggestion = ai_model.suggest(purpose)
    if suggestion is None:
        return redirect("form-create")

    new_form = Form.objects.create(
        owner=request.user, title=title, description=description,
    )
    for i, f in enumerate(suggestion["fields"], start=1):
        Field.objects.create(
            form=new_form,
            field_type=f["field_type"],
            label=f["label"],
            help_text=f.get("help_text", ""),
            placeholder=f.get("placeholder", ""),
            required=f.get("required", False),
            order=i,
            config=f.get("config", {}),
        )
    return redirect("form-detail", slug=new_form.slug)


@login_required
def form_detail(request, slug):
    feedback_form = get_object_or_404(Form, slug=slug, owner=request.user)
    fields = feedback_form.fields.all()
    responses = feedback_form.responses.prefetch_related("answers__field").all()
    share_url = request.build_absolute_uri(
        reverse("form-public", kwargs={"slug": feedback_form.slug})
    )
    return render(request, "survey/form_detail.html", {
        "form_obj": feedback_form,
        "fields": fields,
        "responses": responses,
        "total": responses.count(),
        "share_url": share_url,
    })


@login_required
def form_delete(request, slug):
    feedback_form = get_object_or_404(Form, slug=slug, owner=request.user)
    if request.method == "POST":
        feedback_form.delete()
        return redirect("dashboard")
    return render(request, "survey/form_delete.html", {"form_obj": feedback_form})


@login_required
def field_create(request, slug):
    feedback_form = get_object_or_404(Form, slug=slug, owner=request.user)
    if request.method == "POST":
        form = FieldForm(request.POST)
        if form.is_valid():
            field = form.save(commit=False)
            field.form = feedback_form
            last_order = feedback_form.fields.aggregate(m=Max("order"))["m"] or 0
            field.order = last_order + 1
            field.save()
            return redirect("form-detail", slug=feedback_form.slug)
    else:
        form = FieldForm()
    return render(request, "survey/field_form.html", {
        "form_obj": feedback_form, "form": form, "mode": "create",
    })


@login_required
def field_edit(request, slug, field_id):
    feedback_form = get_object_or_404(Form, slug=slug, owner=request.user)
    field = get_object_or_404(Field, pk=field_id, form=feedback_form)
    if request.method == "POST":
        form = FieldForm(request.POST, instance=field)
        if form.is_valid():
            form.save()
            return redirect("form-detail", slug=feedback_form.slug)
    else:
        form = FieldForm(instance=field)
    return render(request, "survey/field_form.html", {
        "form_obj": feedback_form, "form": form, "field": field, "mode": "edit",
    })


@login_required
@require_http_methods(["POST"])
def field_delete(request, slug, field_id):
    feedback_form = get_object_or_404(Form, slug=slug, owner=request.user)
    field = get_object_or_404(Field, pk=field_id, form=feedback_form)
    field.delete()
    return redirect("form-detail", slug=feedback_form.slug)


@login_required
@require_http_methods(["POST"])
def field_reorder(request, slug, field_id):
    feedback_form = get_object_or_404(Form, slug=slug, owner=request.user)
    field = get_object_or_404(Field, pk=field_id, form=feedback_form)
    direction = request.POST.get("direction")
    siblings = list(feedback_form.fields.all())
    idx = siblings.index(field)
    target = None
    if direction == "up" and idx > 0:
        target = siblings[idx - 1]
    elif direction == "down" and idx < len(siblings) - 1:
        target = siblings[idx + 1]
    if target:
        field.order, target.order = target.order, field.order
        Field.objects.bulk_update([field, target], ["order"])
    return redirect("form-detail", slug=feedback_form.slug)


def form_public(request, slug):
    feedback_form = get_object_or_404(Form, slug=slug)
    return render(request, "survey/form_public.html", {
        "form_obj": feedback_form,
        "fields": feedback_form.fields.all(),
    })


def _validate_answer(field, raw):
    """Return (cleaned_value, error). raw is either a string or a list."""
    is_blank = (raw is None or (isinstance(raw, str) and not raw.strip())
                or (isinstance(raw, list) and not raw))
    if field.required and is_blank:
        return None, f"{field.label} is required."
    if is_blank:
        return ("" if field.field_type not in Field.LIST_TYPES else []), None

    if field.field_type == Field.EMAIL:
        if not EMAIL_RE.match(raw.strip()):
            return None, f"{field.label}: please enter a valid email."
        return raw.strip(), None
    if field.field_type == Field.PHONE:
        if not PHONE_RE.match(raw.strip()):
            return None, f"{field.label}: please enter a valid phone number."
        return raw.strip(), None
    if field.field_type == Field.NUMBER:
        try:
            float(raw)
            return str(raw).strip(), None
        except (TypeError, ValueError):
            return None, f"{field.label}: please enter a number."
    if field.field_type == Field.DATE:
        if not DATE_RE.match(raw.strip()):
            return None, f"{field.label}: please enter a date (YYYY-MM-DD)."
        return raw.strip(), None
    if field.field_type == Field.TIME:
        if not TIME_RE.match(raw.strip()):
            return None, f"{field.label}: please enter a time (HH:MM)."
        return raw.strip(), None
    if field.field_type == Field.RATING:
        try:
            v = int(raw)
            if not 1 <= v <= field.rating_max:
                raise ValueError
            return str(v), None
        except (TypeError, ValueError):
            return None, f"{field.label}: rating must be 1-{field.rating_max}."
    if field.field_type in (Field.MULTIPLE_CHOICE, Field.DROPDOWN):
        if raw not in field.options:
            return None, f"{field.label}: choose one of the options."
        return raw, None
    if field.field_type == Field.CHECKBOXES:
        if not isinstance(raw, list):
            raw = [raw]
        valid = [v for v in raw if v in field.options]
        if not valid and field.required:
            return None, f"{field.label}: choose at least one option."
        return valid, None
    # short/long text fallback
    return str(raw).strip(), None


@require_http_methods(["POST"])
def form_public_submit(request, slug):
    """Handle non-JSON form POSTs (with files) from the public form page."""
    feedback_form = get_object_or_404(Form, slug=slug)
    errors = []
    cleaned = []  # list of (field, value, file_or_None)

    for field in feedback_form.fields.all():
        if field.field_type == Field.FILE:
            uploaded = request.FILES.get(f"field_{field.id}")
            if field.required and not uploaded:
                errors.append(f"{field.label} is required.")
                continue
            cleaned.append((field, "", uploaded))
            continue

        if field.field_type == Field.CHECKBOXES:
            raw = request.POST.getlist(f"field_{field.id}")
        else:
            raw = request.POST.get(f"field_{field.id}", "")
        value, err = _validate_answer(field, raw)
        if err:
            errors.append(err)
        else:
            cleaned.append((field, value, None))

    if errors:
        return render(request, "survey/form_public.html", {
            "form_obj": feedback_form,
            "fields": feedback_form.fields.all(),
            "errors": errors,
            "submitted": request.POST,
        })

    response = Response.objects.create(form=feedback_form)
    for field, value, uploaded in cleaned:
        ans = Answer(response=response, field=field)
        if uploaded is not None:
            ans.file = uploaded
        elif isinstance(value, list):
            ans.value = json.dumps(value)
        else:
            ans.value = value
        ans.save()

    return render(request, "survey/form_success.html", {"form_obj": feedback_form})


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def api_submit(request, slug):
    if request.method == "OPTIONS":
        return _cors(HttpResponse(status=204))

    feedback_form = get_object_or_404(Form, slug=slug)
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return _cors(JsonResponse({"error": "Invalid JSON"}, status=400))

    answers_in = data.get("answers") or {}
    if not isinstance(answers_in, dict):
        return _cors(JsonResponse({"error": "answers must be an object keyed by field id"}, status=400))

    errors = []
    cleaned = []
    for field in feedback_form.fields.all():
        raw = answers_in.get(str(field.id))
        value, err = _validate_answer(field, raw)
        if err:
            errors.append(err)
        else:
            cleaned.append((field, value))

    if errors:
        return _cors(JsonResponse({"errors": errors}, status=400))

    response = Response.objects.create(form=feedback_form)
    for field, value in cleaned:
        if isinstance(value, list):
            Answer.objects.create(response=response, field=field, value=json.dumps(value))
        else:
            Answer.objects.create(response=response, field=field, value=value)

    return _cors(JsonResponse(
        {"id": response.id, "message": "Thanks for your feedback!"},
        status=201,
    ))
