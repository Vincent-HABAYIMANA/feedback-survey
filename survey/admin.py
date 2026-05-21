from django.contrib import admin

from .models import Answer, Field, Form, Response


class FieldInline(admin.TabularInline):
    model = Field
    extra = 0
    fields = ("order", "label", "field_type", "required")


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "slug", "created_at")
    search_fields = ("title", "owner__username")
    readonly_fields = ("slug", "created_at")
    inlines = [FieldInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = ("field", "value", "file")
    readonly_fields = ("field",)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("form", "submitted_at")
    list_filter = ("form",)
    readonly_fields = ("submitted_at",)
    inlines = [AnswerInline]


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ("label", "form", "field_type", "required", "order")
    list_filter = ("field_type", "form")
