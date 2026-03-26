from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("pk", "job_type", "queue_name", "status", "attempt_count", "available_at", "created_at")
    list_filter = ("status", "queue_name", "job_type")
    search_fields = ("job_type", "dedupe_key")
    readonly_fields = ("created_at", "updated_at")
