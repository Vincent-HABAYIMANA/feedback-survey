from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Auth
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(
        template_name="survey/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),

    # Owner pages
    path("dashboard/", views.dashboard, name="dashboard"),
    path("forms/new/", views.form_create, name="form-create"),
    path("forms/ai/suggest/", views.ai_suggest, name="ai-suggest"),
    path("forms/ai/apply/", views.ai_apply, name="ai-apply"),
    path("forms/<slug:slug>/", views.form_detail, name="form-detail"),
    path("forms/<slug:slug>/delete/", views.form_delete, name="form-delete"),
    path("forms/<slug:slug>/fields/new/", views.field_create, name="field-create"),
    path("forms/<slug:slug>/fields/<int:field_id>/edit/", views.field_edit, name="field-edit"),
    path("forms/<slug:slug>/fields/<int:field_id>/delete/", views.field_delete, name="field-delete"),
    path("forms/<slug:slug>/fields/<int:field_id>/move/", views.field_reorder, name="field-reorder"),

    # Public
    path("f/<slug:slug>/", views.form_public, name="form-public"),
    path("f/<slug:slug>/submit/", views.form_public_submit, name="form-public-submit"),

    # JSON API (CORS-enabled, kept for programmatic use)
    path("api/forms/<slug:slug>/submit/", views.api_submit, name="api-submit"),
]
