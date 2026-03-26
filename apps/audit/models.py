from django.db import models
from django.utils import timezone


class AuditLog(models.Model):
    """Trace important GM and system actions."""

    class ActorType(models.TextChoices):
        GM = "gm", "GM"
        SYSTEM = "system", "System"

    actor_type = models.CharField(max_length=10, choices=ActorType.choices)
    actor_label = models.CharField(max_length=255)
    action = models.CharField(max_length=120)
    target_type = models.CharField(max_length=120, blank=True)
    target_id = models.CharField(max_length=120, blank=True)
    details_json = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(default=timezone.now, editable=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"[{self.actor_type}] {self.actor_label}: {self.action}"
