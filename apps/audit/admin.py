"""Admin configuration for the audit app.

AuditLog entries are immutable — all fields are read-only and
no add/delete is permitted.
"""

from django.contrib import admin
from django.http import HttpRequest

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Read-only admin view for audit log entries."""

    list_display = ("created_at", "actor_type", "actor_label", "action", "target_type", "target_id")
    list_filter = ("actor_type", "action", "target_type")
    search_fields = ("actor_label", "action", "target_type", "target_id")
    readonly_fields = (
        "actor_type",
        "actor_label",
        "action",
        "target_type",
        "target_id",
        "details_json",
        "created_at",
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Audit entries are created programmatically, not via admin."""
        return False

    def has_delete_permission(self, request: HttpRequest, obj: AuditLog | None = None) -> bool:
        """Audit entries are immutable and cannot be deleted."""
        return False

    def has_change_permission(self, request: HttpRequest, obj: AuditLog | None = None) -> bool:
        """Audit entries are immutable and cannot be edited."""
        return False
