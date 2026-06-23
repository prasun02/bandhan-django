from django.contrib import admin

from .models import ReturnRequest, ReturnStatusHistory


@admin.action(description="Approve selected returns")
def approve_returns(modeladmin, request, queryset):
    queryset.update(status=ReturnRequest.Status.APPROVED)


@admin.action(description="Reject selected returns")
def reject_returns(modeladmin, request, queryset):
    queryset.update(status=ReturnRequest.Status.REJECTED)


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ("order", "order_item", "quantity", "requested_resolution", "status", "created_at")
    list_filter = ("status", "requested_resolution")
    search_fields = ("order__number", "reason", "description")
    actions = (approve_returns, reject_returns)


admin.site.register(ReturnStatusHistory)
