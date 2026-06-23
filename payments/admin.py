from django.contrib import admin

from .models import Payment, PaymentAttempt


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "method", "status", "amount_paisa", "transaction_id", "updated_at")
    list_filter = ("method", "status")
    search_fields = ("order__number", "transaction_id", "provider_reference")
    readonly_fields = ("created_at", "updated_at")


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = ("payment", "provider", "verified", "created_at")
    readonly_fields = ("request_payload", "response_payload", "created_at")
