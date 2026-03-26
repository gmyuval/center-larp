from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "start_at", "end_at", "price_amount", "registration_open")
    list_filter = ("registration_open", "public_roster_enabled")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
