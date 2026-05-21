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

    # Dashboard + form management (owner-only)
    path("dashboard/", views.dashboard, name="dashboard"),
    path("forms/new/", views.form_create, name="form-create"),
    path("forms/<slug:slug>/", views.form_detail, name="form-detail"),
    path("forms/<slug:slug>/delete/", views.form_delete, name="form-delete"),

    # Public share link
    path("f/<slug:slug>/", views.form_public, name="form-public"),

    # API
    path("api/forms/<slug:slug>/submit/", views.api_submit, name="api-submit"),
]
