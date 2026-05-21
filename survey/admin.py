from django.contrib import admin

from .models import SurveyResponse


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "satisfaction", "age_group", "submitted_at")
    list_filter = ("satisfaction", "age_group", "contact_me")
    search_fields = ("name", "email", "comments")
    readonly_fields = ("submitted_at",)
