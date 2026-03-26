from django.db import models
from django.utils import timezone


class IntegrationEvent(models.Model):
    """Raw vendor payloads for traceability and idempotent processing."""

    class Source(models.TextChoices):
        CARDCOM = "cardcom", "Cardcom"
        MORNING = "morning", "Morning"

    class ProcessingStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        DONE = "done", "Done"
        FAILED = "failed", "Failed"

    source = models.CharField(max_length=20, choices=Source.choices, db_index=True)
    event_type = models.CharField(max_length=100)
    dedupe_key = models.CharField(max_length=255)
    payload_json = models.JSONField(default=dict)
    processing_status = models.CharField(
        max_length=20,
        choices=ProcessingStatus.choices,
        default=ProcessingStatus.PENDING,
        db_index=True,
    )
    error_message = models.TextField(blank=True)

    received_at = models.DateTimeField(default=timezone.now, editable=False)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "dedupe_key"],
                name="unique_source_dedupe_key",
            ),
        ]
        ordering = ["-received_at"]

    def __str__(self) -> str:
        return f"{self.source}:{self.event_type} [{self.dedupe_key}]"
