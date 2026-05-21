from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Field, Form as FeedbackForm


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class FormCreateForm(forms.ModelForm):
    class Meta:
        model = FeedbackForm
        fields = ("title", "description")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Customer satisfaction Q1"}),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Optional. Shown above the form.",
            }),
        }


class FieldForm(forms.ModelForm):
    # User-friendly inputs that we convert into the JSON `config` field.
    options_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "One option per line"}),
        label="Options",
        help_text="One option per line. Used by multiple choice, checkboxes, and dropdown.",
    )
    rating_max = forms.IntegerField(
        required=False, min_value=2, max_value=10, initial=5,
        label="Rating scale max",
        help_text="Top of the rating scale (e.g. 5 means 1-5 stars).",
    )

    class Meta:
        model = Field
        fields = ("field_type", "label", "help_text", "placeholder", "required")
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "What's your question?"}),
            "help_text": forms.TextInput(attrs={"placeholder": "Optional hint shown under the label"}),
            "placeholder": forms.TextInput(attrs={"placeholder": "Optional placeholder text"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance and instance.pk:
            if instance.field_type in Field.NEEDS_OPTIONS:
                self.fields["options_text"].initial = "\n".join(instance.options)
            if instance.field_type == Field.RATING:
                self.fields["rating_max"].initial = instance.rating_max

    def clean(self):
        cleaned = super().clean()
        ftype = cleaned.get("field_type")
        if ftype in Field.NEEDS_OPTIONS:
            options = [
                line.strip() for line in (cleaned.get("options_text") or "").splitlines()
                if line.strip()
            ]
            if len(options) < 2:
                self.add_error("options_text", "Please provide at least 2 options.")
            cleaned["_config"] = {"options": options}
        elif ftype == Field.RATING:
            cleaned["_config"] = {"max": cleaned.get("rating_max") or 5}
        else:
            cleaned["_config"] = {}
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.config = self.cleaned_data.get("_config", {})
        if commit:
            instance.save()
        return instance
