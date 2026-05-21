from django.contrib import admin

from .models import Form, SurveyResponse


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "slug", "created_at")
    search_fields = ("title", "owner__username")
    readonly_fields = ("slug", "created_at")


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "satisfaction", "form", "submitted_at")
    list_filter = ("satisfaction", "age_group", "contact_me", "form")
    search_fields = ("name", "email", "comments")
    readonly_fields = ("submitted_at",)
