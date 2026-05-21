import secrets

from django.conf import settings
from django.db import models


def _gen_slug():
    return secrets.token_urlsafe(8)


class Form(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="forms",
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=32, unique=True, default=_gen_slug)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class SurveyResponse(models.Model):
    AGE_CHOICES = [
        ("Under 18", "Under 18"),
        ("18-24", "18-24"),
        ("25-34", "25-34"),
        ("35-44", "35-44"),
        ("45-54", "45-54"),
        ("55+", "55+"),
    ]

    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name="responses",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=120)
    email = models.EmailField()
    age_group = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True)
    satisfaction = models.PositiveSmallIntegerField()
    likes = models.JSONField(default=list, blank=True)
    comments = models.TextField(blank=True)
    contact_me = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.name} ({self.satisfaction}/5) - {self.submitted_at:%Y-%m-%d %H:%M}"
