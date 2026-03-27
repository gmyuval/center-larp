"""URL patterns for the applications app: form submission and confirmation."""

from django.urls import path

from . import views

app_name = "applications"

urlpatterns = [
    path("apply/", views.ApplicationFormView.as_view(), name="apply"),
    path("apply/thanks/", views.ApplicationThanksView.as_view(), name="thanks"),
]
