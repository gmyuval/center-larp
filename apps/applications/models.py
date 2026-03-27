import uuid

from django.db import models
from django.utils import timezone


class Application(models.Model):
    """A player's application to an event."""

    class GmStatus(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    class PaymentStatus(models.TextChoices):
        NOT_REQUESTED = "not_requested", "Not Requested"
        LINK_CREATED = "link_created", "Link Created"
        LINK_SENT = "link_sent", "Link Sent"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        EXPIRED = "expired", "Expired"
        WAIVED = "waived", "Waived"

    class InvoiceStatus(models.TextChoices):
        NOT_CREATED = "not_created", "Not Created"
        QUEUED = "queued", "Queued"
        CREATED = "created", "Created"
        EMAILED = "emailed", "Emailed"
        FAILED = "failed", "Failed"

    # --- Identity ---
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    event = models.ForeignKey(
        "public_site.Event",
        on_delete=models.PROTECT,
        related_name="applications",
    )

    # --- Contact ---
    full_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)

    # --- Form data ---
    answers_json = models.JSONField(default=dict, blank=True)
    form_version = models.CharField(max_length=50, blank=True)

    # --- Workflow statuses ---
    gm_status = models.CharField(max_length=20, choices=GmStatus.choices, default=GmStatus.SUBMITTED, db_index=True)
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.NOT_REQUESTED,
        db_index=True,
    )
    invoice_status = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.NOT_CREATED,
        db_index=True,
    )

    # --- Roster visibility ---
    is_publicly_published = models.BooleanField(default=False)
    show_character_publicly = models.BooleanField(default=False)
    show_faction_publicly = models.BooleanField(default=False)
    public_character_name = models.CharField(max_length=255, blank=True)
    public_faction_name = models.CharField(max_length=255, blank=True)

    # --- GM notes ---
    gm_notes = models.TextField(blank=True)

    # --- Timestamps ---
    submitted_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submitted_at"]
        indexes = [
            models.Index(fields=["event", "gm_status"]),
            models.Index(fields=["event", "is_publicly_published"]),
        ]

    def __str__(self) -> str:
        return f"{self.display_name} — {self.get_gm_status_display()}"  # pyright: ignore[reportAttributeAccessIssue]
