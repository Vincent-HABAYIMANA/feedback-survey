from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Form as FeedbackForm


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
                "placeholder": "Optional. Shown above the form to people filling it out.",
            }),
        }
