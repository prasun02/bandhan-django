from django.contrib import admin

from .models import Invoice, Order, OrderAddress, OrderItem, OrderSequence, OrderStatusHistory, Shipment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "sku", "unit_price_paisa", "quantity")


class OrderAddressInline(admin.StackedInline):
    model = OrderAddress
    extra = 0


@admin.action(description="Mark selected COD orders paid")
def mark_cod_paid(modeladmin, request, queryset):
    for order in queryset.select_related("payment"):
        if hasattr(order, "payment"):
            order.payment.status = "paid"
            order.payment.save(update_fields=["status", "updated_at"])


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("number", "phone", "status", "grand_total_paisa", "delivery_zone_name", "created_at")
    list_filter = ("status", "delivery_zone_name", "created_at")
    search_fields = ("number", "phone", "email")
    readonly_fields = ("number", "idempotency_token", "stock_reduced_at", "restocked_at", "created_at", "updated_at")
    inlines = (OrderItemInline, OrderAddressInline)
    actions = (mark_cod_paid,)
    date_hierarchy = "created_at"


admin.site.register(OrderItem)
admin.site.register(OrderAddress)
admin.site.register(OrderStatusHistory)
admin.site.register(Shipment)
admin.site.register(Invoice)
admin.site.register(OrderSequence)
