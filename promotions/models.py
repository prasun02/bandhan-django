from django.conf import settings
from django.db import models
from django.utils import timezone

from catalog.models import Category, Product


class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED = "fixed", "Fixed"
        FREE_DELIVERY = "free_delivery", "Free delivery"

    code = models.CharField(max_length=40, unique=True)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    value = models.PositiveIntegerField(default=0)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    minimum_order_paisa = models.PositiveBigIntegerField(default=0)
    maximum_discount_paisa = models.PositiveBigIntegerField(null=True, blank=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    per_customer_limit = models.PositiveIntegerField(default=1)
    products = models.ManyToManyField(Product, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def is_valid_now(self):
        now = timezone.now()
        return self.is_active and self.start_at <= now <= self.end_at


class CouponRedemption(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, related_name="redemptions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    order_number = models.CharField(max_length=40, blank=True)
    redeemed_at = models.DateTimeField(auto_now_add=True)


