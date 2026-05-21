import json

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import FormCreateForm, SignupForm
from .models import Form, SurveyResponse


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
def form_detail(request, slug):
    feedback_form = get_object_or_404(Form, slug=slug, owner=request.user)
    responses = feedback_form.responses.all()
    avg = responses.aggregate(avg=Avg("satisfaction"))["avg"]
    share_url = request.build_absolute_uri(
        reverse("form-public", kwargs={"slug": feedback_form.slug})
    )
    return render(request, "survey/form_detail.html", {
        "form_obj": feedback_form,
        "responses": responses,
        "average": round(avg, 2) if avg else None,
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


def form_public(request, slug):
    feedback_form = get_object_or_404(Form, slug=slug)
    return render(request, "survey/form_public.html", {"form_obj": feedback_form})


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

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    satisfaction = data.get("satisfaction")

    if not name:
        return _cors(JsonResponse({"error": "Name is required"}, status=400))
    if not email or "@" not in email:
        return _cors(JsonResponse({"error": "Valid email is required"}, status=400))
    try:
        satisfaction = int(satisfaction)
        if not 1 <= satisfaction <= 5:
            raise ValueError
    except (TypeError, ValueError):
        return _cors(JsonResponse({"error": "Satisfaction must be 1-5"}, status=400))

    likes = data.get("likes") or []
    if not isinstance(likes, list):
        likes = [str(likes)]

    response = SurveyResponse.objects.create(
        form=feedback_form,
        name=name,
        email=email,
        age_group=(data.get("age_group") or "").strip(),
        satisfaction=satisfaction,
        likes=likes,
        comments=(data.get("comments") or "").strip(),
        contact_me=bool(data.get("contact_me")),
    )

    return _cors(JsonResponse(
        {"id": response.id, "message": "Thanks for your feedback!"},
        status=201,
    ))
