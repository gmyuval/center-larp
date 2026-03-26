import uuid

from django.db import models
from django.utils import timezone

_ACTIVE_STATUS_VALUES = ["created", "sent"]


class PaymentAttempt(models.Model):
    """A single payment link / attempt for an application."""

    class Status(models.TextChoices):
        CREATED = "created", "Created"
        SENT = "sent", "Sent"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        EXPIRED = "expired", "Expired"
        INVALIDATED = "invalidated", "Invalidated"

    ACTIVE_STATUSES = (Status.CREATED, Status.SENT)

    # --- Identity ---
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.PROTECT,
        related_name="payment_attempts",
    )

    # --- Payment details ---
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, default="ILS")
    vendor = models.CharField(max_length=20, default="cardcom")

    # --- Cardcom fields ---
    vendor_low_profile_id = models.CharField(max_length=120, blank=True)
    payment_url = models.URLField(max_length=500, blank=True)

    # --- Status ---
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED, db_index=True)

    # --- Raw responses ---
    raw_create_response_json = models.JSONField(default=dict, blank=True)
    raw_getlpresult_json = models.JSONField(default=dict, blank=True)

    # --- Timestamps ---
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    invalidated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["application"],
                condition=models.Q(status__in=_ACTIVE_STATUS_VALUES),
                name="one_active_attempt_per_application",
            ),
        ]

    def __str__(self) -> str:
        return f"Payment {self.public_id} — {self.get_status_display()}"

    @property
    def is_active(self) -> bool:
        return self.status in self.ACTIVE_STATUSES
