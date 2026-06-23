from django.contrib import admin

from .models import Coupon, CouponRedemption


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_type", "value", "minimum_order_paisa", "is_active", "start_at", "end_at")
    list_filter = ("discount_type", "is_active")
    search_fields = ("code",)
    filter_horizontal = ("products", "categories")


@admin.register(CouponRedemption)
class CouponRedemptionAdmin(admin.ModelAdmin):
    list_display = ("coupon", "user", "order_number", "redeemed_at")
    search_fields = ("coupon__code", "order_number", "user__email")
