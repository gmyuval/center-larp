"""Cardcom payment service: payment page creation and verification."""

import logging
from typing import Any

import httpx
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from apps.applications.models import Application
from apps.public_site.config_loader import ConfigLoader

from .models import PaymentAttempt

logger = logging.getLogger(__name__)


class CardcomService:
    """Handles Cardcom Low Profile payment page creation and verification.

    - ``create_payment_page`` creates a PaymentAttempt, calls the Cardcom
      LowProfile/Create API, stores the response, and emails the player.
    - ``verify_payment`` calls GetLpResult for a given LowProfileId and
      returns the parsed response (used by the job runner in PR 9).
    """

    # ------------------------------------------------------------------
    # Payment page creation
    # ------------------------------------------------------------------

    @classmethod
    def create_payment_page(cls, application: Application) -> PaymentAttempt:
        """Create a Cardcom hosted payment page for the given application.

        Creates a ``PaymentAttempt``, calls the Cardcom API, stores the
        vendor response, emails the player a safe payment link, and
        updates the application's payment status.

        Raises ``ValueError`` if the application already has an active
        payment attempt. Raises ``httpx.HTTPError`` on API failure.
        """
        if PaymentAttempt.objects.filter(
            application=application,
            status__in=PaymentAttempt.ACTIVE_STATUSES,
        ).exists():
            raise ValueError(f"Application {application.public_id} already has an active payment attempt.")

        event_config = ConfigLoader.get_event_config()
        attempt = PaymentAttempt.objects.create(
            application=application,
            amount=application.event.price_amount,
        )

        payload = cls._build_create_payload(attempt, application, event_config)

        try:
            response = httpx.post(
                settings.CARDCOM_LOW_PROFILE_URL,
                json=payload,
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError:
            logger.exception("Cardcom LowProfile/Create failed for attempt %s", attempt.public_id)
            attempt.status = PaymentAttempt.Status.FAILED
            attempt.save(update_fields=["status", "updated_at"])
            raise

        low_profile_id = str(data.get("LowProfileId", ""))
        payment_url = str(data.get("Url", ""))

        if not low_profile_id or not payment_url:
            logger.error(
                "Cardcom returned empty LowProfileId or Url for attempt %s: %s",
                attempt.public_id,
                data,
            )
            attempt.status = PaymentAttempt.Status.FAILED
            attempt.raw_create_response_json = data
            attempt.save(update_fields=["status", "raw_create_response_json", "updated_at"])
            raise ValueError("Cardcom returned an incomplete response (missing LowProfileId or Url).")

        attempt.vendor_low_profile_id = low_profile_id
        attempt.payment_url = payment_url
        attempt.raw_create_response_json = data
        attempt.status = PaymentAttempt.Status.SENT
        attempt.sent_at = timezone.now()
        attempt.save(
            update_fields=[
                "vendor_low_profile_id",
                "payment_url",
                "raw_create_response_json",
                "status",
                "sent_at",
            ]
        )

        email_sent = cls._send_payment_email(application, attempt, event_config)

        application.payment_status = (
            Application.PaymentStatus.LINK_SENT if email_sent else Application.PaymentStatus.LINK_CREATED
        )
        application.save(update_fields=["payment_status", "updated_at"])

        return attempt

    @classmethod
    def _build_create_payload(
        cls,
        attempt: PaymentAttempt,
        application: Application,
        event_config: Any,
    ) -> dict[str, Any]:
        """Build the JSON payload for Cardcom LowProfile/Create."""
        base_url = settings.APP_BASE_URL.rstrip("/")
        return {
            "TerminalNumber": settings.CARDCOM_TERMINAL_NUMBER,
            "ApiName": settings.CARDCOM_API_NAME,
            "ReturnValue": str(attempt.public_id),
            "Amount": str(attempt.amount),
            "SuccessRedirectUrl": f"{base_url}/payment/return/success/",
            "FailedRedirectUrl": f"{base_url}/payment/return/failure/",
            "WebhookUrl": f"{base_url}/webhooks/cardcom/low-profile/",
            "Language": event_config.cardcom_language,
            "Operation": "ChargeOnly",
            "DocTypeToCreate": 0,
            "IsRefundsSupport": "False",
            "Document": {
                "Name": application.full_name,
                "Email": application.email,
                "Phone": application.phone,
            },
        }

    @staticmethod
    def _send_payment_email(
        application: Application,
        attempt: PaymentAttempt,
        event_config: Any,
    ) -> bool:
        """Send the payment link email to the applicant.

        Returns True if the email was sent successfully, False otherwise.
        """
        base_url = settings.APP_BASE_URL.rstrip("/")
        pay_url = f"{base_url}/pay/{attempt.public_id}/"

        try:
            subject = f"קישור לתשלום — {event_config.title}"
            body = render_to_string(
                "emails/payment_link.txt",
                {
                    "application": application,
                    "event": event_config,
                    "pay_url": pay_url,
                },
            )
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[application.email],
                fail_silently=False,
            )
        except Exception:
            logger.exception(
                "Failed to send payment link email for application %s",
                application.public_id,
            )
            return False
        return True

    # ------------------------------------------------------------------
    # Payment verification (called by job runner in PR 9)
    # ------------------------------------------------------------------

    @classmethod
    def verify_payment(cls, low_profile_id: str) -> dict[str, Any]:
        """Call Cardcom GetLpResult to verify a payment.

        Returns the parsed JSON response. The caller is responsible for
        interpreting the ``ResponseCode`` and updating model state.
        """
        response = httpx.get(
            settings.CARDCOM_GET_LP_RESULT_URL,
            params={
                "TerminalNumber": settings.CARDCOM_TERMINAL_NUMBER,
                "ApiName": settings.CARDCOM_API_NAME,
                "LowProfileId": low_profile_id,
            },
            timeout=30.0,
        )
        response.raise_for_status()
        result: dict[str, Any] = response.json()
        return result

    # ------------------------------------------------------------------
    # Invalidation
    # ------------------------------------------------------------------

    @staticmethod
    def invalidate_active_attempt(application: Application) -> PaymentAttempt | None:
        """Invalidate the current active payment attempt for an application.

        Returns the invalidated attempt, or None if no active attempt exists.
        """
        active = (
            PaymentAttempt.objects.filter(
                application=application,
                status__in=PaymentAttempt.ACTIVE_STATUSES,
            )
            .select_for_update()
            .first()
        )

        if active is not None:
            active.status = PaymentAttempt.Status.INVALIDATED
            active.invalidated_at = timezone.now()
            active.save(update_fields=["status", "invalidated_at"])

        return active
