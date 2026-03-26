from django.db import models
from django.utils import timezone


class Event(models.Model):
    """Event-level configuration. One row per LARP event."""

    slug = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    location_text = models.CharField(max_length=255, blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    price_amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, default="ILS")
    registration_open = models.BooleanField(default=False)
    public_roster_enabled = models.BooleanField(default=False)

    MORNING_DOC_TYPE_CHOICES = [
        ("305", "Tax Invoice (305)"),
        ("320", "Receipt (320)"),
        ("400", "Receipt/Invoice (400)"),
    ]
    morning_document_type = models.CharField(max_length=3, choices=MORNING_DOC_TYPE_CHOICES, default="320")
    cardcom_language = models.CharField(max_length=5, default="he")
    landing_template = models.CharField(max_length=120, blank=True, help_text="Template override for landing page")

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_at"]

    def __str__(self) -> str:
        return self.title


class EventManager:
    """Helper for retrieving the current event."""

    @staticmethod
    def get_current() -> Event | None:
        return Event.objects.filter(registration_open=True).order_by("-start_at").first()
