from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "email",
        "event",
        "gm_status",
        "payment_status",
        "invoice_status",
        "is_publicly_published",
        "submitted_at",
    )
    list_select_related = ("event",)
    list_filter = ("gm_status", "payment_status", "invoice_status", "is_publicly_published", "event")
    search_fields = ("full_name", "display_name", "email", "phone")
    readonly_fields = ("public_id", "created_at", "updated_at")
