"""URL patterns for payment links, Cardcom webhook, and return pages."""

from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("pay/<uuid:token>/", views.PaymentLinkRedirectView.as_view(), name="pay"),
    path("webhooks/cardcom/low-profile/", views.CardcomWebhookView.as_view(), name="cardcom-webhook"),
    path("payment/return/success/", views.PaymentReturnSuccessView.as_view(), name="return-success"),
    path("payment/return/failure/", views.PaymentReturnFailureView.as_view(), name="return-failure"),
]
