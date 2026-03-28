"""Views for payment link redirect and Cardcom webhook."""

import json
import logging
from typing import Any
from uuid import UUID

from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from apps.jobs.models import Job

from .integration_event import IntegrationEvent
from .models import PaymentAttempt

logger = logging.getLogger(__name__)


class PaymentLinkRedirectView(View):
    """Resolve a PaymentAttempt by UUID and redirect to the Cardcom payment page.

    If the attempt is active and has a payment URL, redirect.
    Otherwise show an informational error.
    """

    def get(self, request: HttpRequest, token: UUID) -> HttpResponse:
        """Look up the payment attempt and redirect or show error."""
        attempt = get_object_or_404(PaymentAttempt, public_id=token)

        if attempt.is_active and attempt.payment_url:
            return redirect(attempt.payment_url)

        status_label = attempt.get_status_display()  # pyright: ignore[reportAttributeAccessIssue]
        return HttpResponse(
            f"קישור התשלום אינו פעיל ({status_label}). נא ליצור קשר עם הצוות.",
            status=410,
            content_type="text/plain; charset=utf-8",
        )


@method_decorator(csrf_exempt, name="dispatch")
class CardcomWebhookView(View):
    """Receive Cardcom Low Profile webhook notifications.

    Persists the raw payload as an IntegrationEvent for idempotent
    processing, enqueues a verification job, and returns HTTP 200
    immediately so Cardcom does not retry.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle webhook POST from Cardcom."""
        try:
            payload: dict[str, Any] = json.loads(request.body)
        except json.JSONDecodeError, ValueError:
            logger.warning("Cardcom webhook: invalid JSON body")
            return HttpResponse(status=400)

        low_profile_id = str(payload.get("lowProfileId", payload.get("LowProfileId", "")))
        if not low_profile_id:
            logger.warning("Cardcom webhook: missing lowProfileId in payload")
            return HttpResponse(status=400)

        try:
            IntegrationEvent.objects.create(
                source=IntegrationEvent.Source.CARDCOM,
                event_type="low_profile_notification",
                dedupe_key=low_profile_id,
                payload_json=payload,
            )
        except IntegrityError:
            logger.info("Cardcom webhook: duplicate event for lowProfileId=%s", low_profile_id)

        Job.objects.get_or_create(
            dedupe_key=f"verify_payment:{low_profile_id}",
            defaults={
                "job_type": "verify_payment",
                "payload_json": {"low_profile_id": low_profile_id},
            },
        )

        return HttpResponse(status=200)

    def get(self, request: HttpRequest) -> HttpResponse:
        """Reject GET requests (Cardcom only sends POST)."""
        return HttpResponse(status=405)


class PaymentReturnSuccessView(TemplateView):
    """Informational success page shown after Cardcom redirects the browser.

    This page does NOT change any payment state — verification happens
    server-side via the webhook + job runner.
    """

    template_name = "public_site/payment_return.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add status context for the template."""
        context = super().get_context_data(**kwargs)
        context["status"] = "success"
        context["title"] = "תודה!"
        context["message"] = "אם התשלום הושלם בהצלחה, נשלח אישור במייל בהקדם."
        return context


class PaymentReturnFailureView(TemplateView):
    """Informational failure page shown after Cardcom redirects the browser."""

    template_name = "public_site/payment_return.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add status context for the template."""
        context = super().get_context_data(**kwargs)
        context["status"] = "failure"
        context["title"] = "התשלום לא הושלם"
        context["message"] = "ניתן לנסות שוב דרך הקישור שנשלח במייל, או ליצור קשר עם הצוות."
        return context
