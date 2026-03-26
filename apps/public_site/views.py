from typing import Any

from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from .config_loader import ConfigLoader


class LivenessView(View):
    def get(self, request: Any) -> JsonResponse:
        return JsonResponse({"status": "ok"})


class ReadinessView(View):
    def get(self, request: Any) -> JsonResponse:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return JsonResponse({"status": "ok"})
        except Exception:
            return JsonResponse({"status": "unavailable"}, status=503)


class LandingPageView(TemplateView):
    template_name = "public_site/landing.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        config = ConfigLoader.get_event_config()
        context["event"] = config
        context["landing"] = config.landing
        context["factions"] = config.factions
        return context
