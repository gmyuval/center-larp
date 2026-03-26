from django.db import models
from django.utils import timezone


class Job(models.Model):
    """DB-backed outbox for background work without Redis."""

    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        PROCESSING = "processing", "Processing"
        DONE = "done", "Done"
        FAILED = "failed", "Failed"

    queue_name = models.CharField(max_length=100, default="default", db_index=True)
    job_type = models.CharField(max_length=120)
    payload_json = models.JSONField(default=dict, blank=True)
    dedupe_key = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED, db_index=True)
    attempt_count = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=3)
    available_at = models.DateTimeField(default=timezone.now, db_index=True)
    locked_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["available_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["dedupe_key"],
                condition=~models.Q(dedupe_key=""),
                name="unique_non_empty_dedupe_key",
            ),
        ]

    def __str__(self) -> str:
        return f"Job {self.pk} [{self.job_type}] — {self.get_status_display()}"
