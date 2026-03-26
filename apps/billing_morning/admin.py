from django.contrib import admin
from django.http import HttpRequest

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("document_number", "application", "document_type", "status", "created_at")
    list_select_related = ("application",)
    list_filter = ("status", "document_type")
    search_fields = ("vendor_document_id", "document_number")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Documents must only be created by the billing system after verified payment."""
        return False
