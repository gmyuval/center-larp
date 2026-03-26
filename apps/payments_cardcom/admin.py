from django.contrib import admin

from .integration_event import IntegrationEvent
from .models import PaymentAttempt


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = ("public_id", "application", "amount", "status", "created_at")
    list_select_related = ("application",)
    list_filter = ("status", "vendor")
    search_fields = ("public_id", "vendor_low_profile_id")
    readonly_fields = ("public_id", "created_at")


@admin.register(IntegrationEvent)
class IntegrationEventAdmin(admin.ModelAdmin):
    list_display = ("source", "event_type", "dedupe_key", "processing_status", "received_at")
    list_filter = ("source", "processing_status")
    search_fields = ("dedupe_key", "event_type")
    readonly_fields = ("received_at",)
