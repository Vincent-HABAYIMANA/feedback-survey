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


class Field(models.Model):
    SHORT_TEXT = "short_text"
    LONG_TEXT = "long_text"
    EMAIL = "email"
    PHONE = "phone"
    NUMBER = "number"
    RATING = "rating"
    MULTIPLE_CHOICE = "multiple_choice"
    CHECKBOXES = "checkboxes"
    DROPDOWN = "dropdown"
    DATE = "date"
    TIME = "time"
    FILE = "file"

    TYPE_CHOICES = [
        (SHORT_TEXT, "Short text"),
        (LONG_TEXT, "Long text (paragraph)"),
        (EMAIL, "Email"),
        (PHONE, "Phone"),
        (NUMBER, "Number"),
        (RATING, "Rating (stars)"),
        (MULTIPLE_CHOICE, "Multiple choice (pick one)"),
        (CHECKBOXES, "Checkboxes (pick many)"),
        (DROPDOWN, "Dropdown"),
        (DATE, "Date"),
        (TIME, "Time"),
        (FILE, "File upload"),
    ]

    # Field types whose answer is a list (stored as JSON list)
    LIST_TYPES = {CHECKBOXES}
    # Field types that need options
    NEEDS_OPTIONS = {MULTIPLE_CHOICE, CHECKBOXES, DROPDOWN}

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="fields")
    field_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    label = models.CharField(max_length=200)
    help_text = models.CharField(max_length=300, blank=True)
    placeholder = models.CharField(max_length=200, blank=True)
    required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    # For multi-choice / checkboxes / dropdown: list of option strings.
    # For rating: {"max": 5}. Other types: {}.
    config = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.label} ({self.get_field_type_display()})"

    @property
    def options(self):
        if self.field_type in self.NEEDS_OPTIONS:
            return self.config.get("options", [])
        return []

    @property
    def rating_max(self):
        return int(self.config.get("max", 5)) if self.field_type == self.RATING else None

    @property
    def rating_range_reversed(self):
        if self.field_type != self.RATING:
            return []
        return list(range(self.rating_max, 0, -1))


class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="responses")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Response to {self.form.title} @ {self.submitted_at:%Y-%m-%d %H:%M}"


class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name="answers")
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="answers")
    # Stores text, JSON-encoded list, or path-like string. Empty for file answers.
    value = models.TextField(blank=True)
    file = models.FileField(upload_to="responses/%Y/%m/", blank=True, null=True)

    class Meta:
        ordering = ["field__order", "id"]

    def display(self):
        from django.utils.safestring import mark_safe
        from django.utils.html import escape

        if self.field.field_type == Field.FILE and self.file:
            return mark_safe(f'<a href="{self.file.url}" target="_blank">{escape(self.file.name.split("/")[-1])}</a>')
        if self.field.field_type in Field.LIST_TYPES:
            try:
                import json
                items = json.loads(self.value) if self.value else []
                return ", ".join(str(x) for x in items)
            except (ValueError, TypeError):
                return self.value
        return self.value or "—"
