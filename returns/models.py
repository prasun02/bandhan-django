from django.conf import settings
from django.db import models

from orders.models import Order, OrderItem


class ReturnRequest(models.Model):
    class Resolution(models.TextChoices):
        REFUND = "refund", "Refund"
        REPLACEMENT = "replacement", "Replacement"
        STORE_CREDIT = "store_credit", "Store credit"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        RECEIVED = "received", "Received"
        COMPLETED = "completed", "Completed"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="return_requests")
    order_item = models.ForeignKey(OrderItem, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    reason = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="returns/", blank=True)
    requested_resolution = models.CharField(max_length=20, choices=Resolution.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)


class ReturnStatusHistory(models.Model):
    return_request = models.ForeignKey(ReturnRequest, on_delete=models.CASCADE, related_name="history")
    status = models.CharField(max_length=20, choices=ReturnRequest.Status.choices)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
