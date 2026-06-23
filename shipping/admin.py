from django.contrib import admin

from .models import DeliveryZone


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "charge_paisa", "free_delivery_threshold_paisa", "delivery_estimate", "is_active")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
