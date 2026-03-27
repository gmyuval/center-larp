"""Application submission service: record creation and email notifications."""

import logging
from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.public_site.config_loader import EventConfig, FormSchemaConfig
from apps.public_site.models import Event

from .constants import CONTACT_FIELD_KEYS
from .models import Application

logger = logging.getLogger(__name__)


class ApplicationService:
    """Handles the full application submission flow.

    Responsibilities:
    - Create an ``Application`` record from validated form data.
    - Send a confirmation email to the applicant.
    - Send a notification email to the GM team.
    """

    def submit(
        self,
        cleaned_data: dict[str, Any],
        event: Event,
        event_config: EventConfig,
        form_schema: FormSchemaConfig,
    ) -> Application:
        """Process a validated application submission.

        Creates the database record, then sends both the applicant
        confirmation and the GM notification emails.
        """
        application = self._create_application(cleaned_data, event, form_schema)
        self._send_confirmation_email(application, event_config)
        self._send_gm_notification(application, event_config)
        return application

    # ------------------------------------------------------------------
    # Record creation
    # ------------------------------------------------------------------

    @staticmethod
    def _create_application(
        cleaned_data: dict[str, Any],
        event: Event,
        form_schema: FormSchemaConfig,
    ) -> Application:
        """Persist a new Application from validated form data.

        Contact fields are stored as dedicated model columns; all
        remaining answers go into ``answers_json``.
        """
        contact_data = {key: cleaned_data.get(key, "") for key in CONTACT_FIELD_KEYS}
        answers = {
            key: value
            for key, value in cleaned_data.items()
            if key not in CONTACT_FIELD_KEYS and key != form_schema.spam_protection.honeypot_field
        }

        return Application.objects.create(
            event=event,
            full_name=contact_data.get("full_name", ""),
            display_name=contact_data.get("display_name", ""),
            email=contact_data.get("email", ""),
            phone=contact_data.get("phone", ""),
            answers_json=answers,
            form_version=str(form_schema.version),
        )

    # ------------------------------------------------------------------
    # Emails
    # ------------------------------------------------------------------

    @staticmethod
    def _send_confirmation_email(application: Application, event_config: EventConfig) -> None:
        """Send a confirmation email to the applicant.

        Failures are logged but not re-raised — the application is
        already saved, so email issues should not block the user.
        """
        subject = f"הרשמתך התקבלה — {event_config.title}"
        body = render_to_string(
            "emails/applicant_confirmation.txt",
            {
                "application": application,
                "event": event_config,
            },
        )
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[application.email],
                fail_silently=False,
            )
        except Exception:
            logger.exception("Failed to send confirmation email to %s", application.email)

    @staticmethod
    def _send_gm_notification(application: Application, event_config: EventConfig) -> None:
        """Send a notification email to the GM team with application details.

        Skips silently when no GM recipients are configured.
        """
        recipients = event_config.emails.gm_notification_to
        if not recipients:
            logger.warning("No GM notification recipients configured — skipping notification")
            return

        subject = f"הרשמה חדשה — {application.display_name}"
        body = render_to_string(
            "emails/gm_notification.txt",
            {
                "application": application,
                "event": event_config,
                "admin_url": f"/gm/applications/application/{application.pk}/change/",
            },
        )
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently=False,
            )
        except Exception:
            logger.exception("Failed to send GM notification for application %s", application.pk)
