from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("actor_type", "actor_label", "action", "target_type", "target_id", "created_at")
    list_filter = ("actor_type", "action")
    search_fields = ("actor_label", "action", "target_type", "target_id")
    readonly_fields = ("created_at",)
