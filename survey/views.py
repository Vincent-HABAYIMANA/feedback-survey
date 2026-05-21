import json
from pathlib import Path

from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import SurveyResponse


def _cors(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def submit(request):
    if request.method == "OPTIONS":
        return _cors(HttpResponse(status=204))

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


@require_http_methods(["GET"])
def stats(request):
    qs = SurveyResponse.objects.all()
    total = qs.count()
    avg = qs.aggregate(avg=Avg("satisfaction"))["avg"]
    return _cors(JsonResponse({
        "total_responses": total,
        "average_satisfaction": round(avg, 2) if avg else None,
    }))


@require_http_methods(["GET"])
def form_page(request):
    html_path = Path(__file__).resolve().parent.parent / "survey_form.html"
    if not html_path.exists():
        return HttpResponse("survey_form.html not found", status=404)
    return HttpResponse(html_path.read_text(encoding="utf-8"))
