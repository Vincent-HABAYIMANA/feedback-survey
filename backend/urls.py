from django.contrib import admin
from django.urls import include, path

from survey.views import form_page

urlpatterns = [
    path("", form_page, name="form"),
    path("admin/", admin.site.urls),
    path("api/", include("survey.urls")),
]
