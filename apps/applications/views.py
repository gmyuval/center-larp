"""Views for the public application form and confirmation page."""

import logging
from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseBase, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from apps.public_site.config_loader import ConfigLoader, EventConfig, FormSchemaConfig
from apps.public_site.models import Event

from .forms import ApplicationForm
from .services import ApplicationService

logger = logging.getLogger(__name__)


class ApplicationFormView(FormView):
    """Render and process the public application form.

    GET renders an empty form; POST validates input, creates an
    ``Application`` record, sends emails, and redirects to the
    confirmation page.  Access is gated on ``registration_open``
    and requires an active ``Event`` in the database.
    """

    template_name = "public_site/apply.html"
    event: Event

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """Load configuration and gate access before handling the request."""
        self.event_config: EventConfig = ConfigLoader.get_event_config()
        if not self.event_config.registration_open:
            return redirect("public_site:landing")

        self.form_schema: FormSchemaConfig = ConfigLoader.get_form_schema()

        event = Event.objects.filter(
            slug=self.event_config.slug,
            registration_open=True,
        ).first()
        if event is None:
            logger.error("No active event found in database for slug=%s", self.event_config.slug)
            return HttpResponse(
                "Event not configured. Please contact the organizers.",
                status=503,
                content_type="text/plain; charset=utf-8",
            )
        self.event = event

        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class: type | None = None) -> ApplicationForm:
        """Return an ``ApplicationForm`` initialised from the YAML schema."""
        return ApplicationForm(**self.get_form_kwargs(), schema=self.form_schema)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add event metadata and form chrome to the template context."""
        context = super().get_context_data(**kwargs)
        context["event"] = self.event_config
        context["form_title"] = self.form_schema.title
        context["submit_button"] = self.form_schema.submit_button
        context["honeypot_field"] = self.form_schema.spam_protection.honeypot_field
        return context

    def form_valid(self, form: ApplicationForm) -> HttpResponseRedirect:
        """Create the application and redirect to the thank-you page."""
        service = ApplicationService()
        service.submit(
            cleaned_data=form.cleaned_data,
            event=self.event,
            event_config=self.event_config,
            form_schema=self.form_schema,
        )
        return redirect("applications:thanks")


class ApplicationThanksView(TemplateView):
    """Confirmation page shown after a successful application submission."""

    template_name = "public_site/apply_thanks.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add the current event config to the template context."""
        context = super().get_context_data(**kwargs)
        context["event"] = ConfigLoader.get_event_config()
        return context
