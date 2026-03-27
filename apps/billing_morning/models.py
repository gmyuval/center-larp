from django.db import models
from django.utils import timezone


class Document(models.Model):
    """A Morning accounting document created after verified payment."""

    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        CREATED = "created", "Created"
        EMAILED = "emailed", "Emailed"
        FAILED = "failed", "Failed"

    # --- Relations ---
    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.PROTECT,
        related_name="documents",
    )
    payment_attempt = models.OneToOneField(
        "payments_cardcom.PaymentAttempt",
        on_delete=models.PROTECT,
        related_name="document",
    )

    # --- Vendor info ---
    vendor = models.CharField(max_length=20, default="morning")
    document_type = models.CharField(max_length=10, blank=True)
    vendor_document_id = models.CharField(max_length=120, blank=True)
    document_number = models.CharField(max_length=50, blank=True)

    # --- Status ---
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED, db_index=True)

    # --- Raw response ---
    raw_response_json = models.JSONField(default=dict, blank=True)

    # --- Timestamps ---
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    emailed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        label = self.document_number or self.vendor_document_id or "pending"
        return f"Document {label} — {self.get_status_display()}"  # pyright: ignore[reportAttributeAccessIssue]
