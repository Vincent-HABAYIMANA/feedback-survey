from django.urls import path

from . import views

urlpatterns = [
    path("submit/", views.submit, name="survey-submit"),
    path("stats/", views.stats, name="survey-stats"),
]
