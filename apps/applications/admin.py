"""Admin configuration for the applications app.

Provides a rich GM interface for managing player applications:
fieldsets, custom actions with state-transition guards, read-only
inlines for payment attempts and documents, and audit logging.
"""

from django.contrib import admin, messages
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils import timezone

from apps.audit.services import AuditService
from apps.billing_morning.models import Document
from apps.payments_cardcom.models import PaymentAttempt

from .constants import APPROVABLE_STATUSES, PUBLISHABLE_STATUSES, REJECTABLE_STATUSES
from .models import Application


class PaymentAttemptInline(admin.TabularInline):
    """Read-only inline showing payment attempts on the Application detail page."""

    model = PaymentAttempt
    extra = 0
    can_delete = False
    fields = ("public_id", "amount", "status", "vendor_low_profile_id", "created_at", "paid_at")
    readonly_fields = ("public_id", "amount", "status", "vendor_low_profile_id", "created_at", "paid_at")
    show_change_link = True

    def has_add_permission(self, request: HttpRequest, obj: Application | None = None) -> bool:
        """Prevent adding payment attempts directly from the inline."""
        return False


class DocumentInline(admin.TabularInline):
    """Read-only inline showing Morning documents on the Application detail page."""

    model = Document
    extra = 0
    can_delete = False
    fields = ("document_type", "document_number", "vendor_document_id", "status", "created_at")
    readonly_fields = ("document_type", "document_number", "vendor_document_id", "status", "created_at")
    show_change_link = True

    def has_add_permission(self, request: HttpRequest, obj: Application | None = None) -> bool:
        """Prevent adding documents directly from the inline."""
        return False


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Full-featured admin for managing player applications."""

    # ------------------------------------------------------------------
    # List view
    # ------------------------------------------------------------------

    list_display = (
        "display_name",
        "full_name",
        "email",
        "event",
        "gm_status",
        "payment_status",
        "invoice_status",
        "is_publicly_published",
        "submitted_at",
    )
    list_select_related = ("event",)
    list_filter = (
        "gm_status",
        "payment_status",
        "invoice_status",
        "is_publicly_published",
        "event",
    )
    search_fields = ("full_name", "display_name", "email", "phone")
    list_per_page = 50
    ordering = ("-submitted_at",)

    # ------------------------------------------------------------------
    # Detail view — fieldsets
    # ------------------------------------------------------------------

    fieldsets = (
        (
            "Contact",
            {
                "fields": ("full_name", "display_name", "email", "phone"),
            },
        ),
        (
            "Application Data",
            {
                "fields": ("event", "public_id", "answers_json", "form_version"),
            },
        ),
        (
            "Workflow",
            {
                "fields": ("gm_status", "payment_status", "invoice_status"),
            },
        ),
        (
            "Public Roster",
            {
                "fields": (
                    "is_publicly_published",
                    "show_character_publicly",
                    "public_character_name",
                    "show_faction_publicly",
                    "public_faction_name",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "GM Notes",
            {
                "fields": ("gm_notes",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "submitted_at",
                    "approved_at",
                    "rejected_at",
                    "paid_at",
                    "published_at",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = (
        "gm_status",
        "is_publicly_published",
        "show_character_publicly",
        "show_faction_publicly",
        "public_id",
        "answers_json",
        "form_version",
        "submitted_at",
        "approved_at",
        "rejected_at",
        "paid_at",
        "published_at",
        "created_at",
        "updated_at",
    )

    inlines = (PaymentAttemptInline, DocumentInline)

    # ------------------------------------------------------------------
    # Admin actions
    # ------------------------------------------------------------------

    actions = [
        "action_approve",
        "action_reject",
        "action_publish",
        "action_unpublish",
        "action_show_character",
        "action_hide_character",
        "action_show_faction",
        "action_hide_faction",
    ]

    @admin.action(description="Approve selected applications")
    def action_approve(self, request: HttpRequest, queryset: QuerySet[Application]) -> None:
        """Transition selected applications from submitted to approved."""
        initial_count = queryset.count()
        now = timezone.now()

        with transaction.atomic():
            eligible = queryset.select_for_update().filter(gm_status__in=APPROVABLE_STATUSES)
            for application in eligible:
                previous_status = application.gm_status
                application.gm_status = Application.GmStatus.APPROVED
                application.approved_at = now
                application.save(update_fields=["gm_status", "approved_at", "updated_at"])
                AuditService.log_gm_action(
                    request=request,
                    action="approve",
                    target=application,
                    details={"previous_status": previous_status},
                )
            updated = eligible.count()

        skipped = initial_count - updated
        if updated:
            self.message_user(request, f"{updated} application(s) approved.", messages.SUCCESS)
        if skipped:
            self.message_user(
                request,
                f"{skipped} application(s) skipped (not in submitted status).",
                messages.WARNING,
            )

    @admin.action(description="Reject selected applications")
    def action_reject(self, request: HttpRequest, queryset: QuerySet[Application]) -> None:
        """Transition selected applications from submitted to rejected."""
        initial_count = queryset.count()
        now = timezone.now()

        with transaction.atomic():
            eligible = queryset.select_for_update().filter(gm_status__in=REJECTABLE_STATUSES)
            for application in eligible:
                previous_status = application.gm_status
                application.gm_status = Application.GmStatus.REJECTED
                application.rejected_at = now
                application.save(update_fields=["gm_status", "rejected_at", "updated_at"])
                AuditService.log_gm_action(
                    request=request,
                    action="reject",
                    target=application,
                    details={"previous_status": previous_status},
                )
            updated = eligible.count()

        skipped = initial_count - updated
        if updated:
            self.message_user(request, f"{updated} application(s) rejected.", messages.SUCCESS)
        if skipped:
            self.message_user(
                request,
                f"{skipped} application(s) skipped (not in submitted status).",
                messages.WARNING,
            )

    @admin.action(description="Publish selected to public roster")
    def action_publish(self, request: HttpRequest, queryset: QuerySet[Application]) -> None:
        """Publish approved applications to the public roster."""
        initial_count = queryset.count()
        now = timezone.now()

        with transaction.atomic():
            eligible = queryset.select_for_update().filter(
                gm_status__in=PUBLISHABLE_STATUSES,
                is_publicly_published=False,
            )
            for application in eligible:
                application.is_publicly_published = True
                application.published_at = now
                application.save(update_fields=["is_publicly_published", "published_at", "updated_at"])
                AuditService.log_gm_action(
                    request=request,
                    action="publish",
                    target=application,
                )
            updated = eligible.count()

        skipped = initial_count - updated
        if updated:
            self.message_user(request, f"{updated} application(s) published.", messages.SUCCESS)
        if skipped:
            self.message_user(
                request,
                f"{skipped} application(s) skipped (not approved or already published).",
                messages.WARNING,
            )

    @admin.action(description="Unpublish selected from public roster")
    def action_unpublish(self, request: HttpRequest, queryset: QuerySet[Application]) -> None:
        """Remove selected applications from the public roster."""
        initial_count = queryset.count()

        with transaction.atomic():
            eligible = queryset.select_for_update().filter(is_publicly_published=True)
            for application in eligible:
                application.is_publicly_published = False
                application.save(update_fields=["is_publicly_published", "updated_at"])
                AuditService.log_gm_action(
                    request=request,
                    action="unpublish",
                    target=application,
                )
            updated = eligible.count()

        skipped = initial_count - updated
        if updated:
            self.message_user(request, f"{updated} application(s) unpublished.", messages.SUCCESS)
        if skipped:
            self.message_user(
                request,
                f"{skipped} application(s) skipped (not currently published).",
                messages.WARNING,
            )

    @admin.action(description="Show character name publicly")
    def action_show_character(self, request: HttpRequest, queryset: QuerySet[Application]) -> None:
        """Enable public character name visibility for selected applications."""
        self._report_toggle(request, queryset, "show_character_publicly", True)

    @admin.action(description="Hide character name publicly")
    def action_hide_character(self, request: HttpRequest, queryset: QuerySet[Application]) -> None:
        """Disable public character name visibility for selected applications."""
        self._report_toggle(request, queryset, "show_character_publicly", False)

    @admin.action(description="Show faction publicly")
    def action_show_faction(self, request: HttpRequest, queryset: QuerySet[Application]) -> None:
        """Enable public faction visibility for selected applications."""
        self._report_toggle(request, queryset, "show_faction_publicly", True)

    @admin.action(description="Hide faction publicly")
    def action_hide_faction(self, request: HttpRequest, queryset: QuerySet[Application]) -> None:
        """Disable public faction visibility for selected applications."""
        self._report_toggle(request, queryset, "show_faction_publicly", False)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _report_toggle(
        self,
        request: HttpRequest,
        queryset: QuerySet[Application],
        field: str,
        value: bool,
    ) -> None:
        """Run a visibility toggle and report the result to the GM."""
        updated = self._toggle_visibility(request, queryset, field, value)
        if updated:
            self.message_user(request, f"{updated} application(s) updated.", messages.SUCCESS)
        else:
            self.message_user(request, "No applications needed updating.", messages.INFO)

    @staticmethod
    def _toggle_visibility(
        request: HttpRequest,
        queryset: QuerySet[Application],
        field: str,
        value: bool,
    ) -> int:
        """Toggle a boolean visibility field and log an audit entry for each change."""
        action_label = f"set_{field}={'on' if value else 'off'}"
        count = 0
        with transaction.atomic():
            for application in queryset.select_for_update():
                if getattr(application, field) != value:
                    setattr(application, field, value)
                    application.save(update_fields=[field, "updated_at"])
                    AuditService.log_gm_action(
                        request=request,
                        action=action_label,
                        target=application,
                        details={field: value},
                    )
                    count += 1
        return count
