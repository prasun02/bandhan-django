import uuid

from django.conf import settings
from django.db import models

from catalog.models import Product, ProductVariant
from promotions.models import Coupon


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name="carts")
    session_key = models.UUIDField(default=uuid.uuid4, db_index=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["user", "session_key"])]

    def __str__(self):
        return f"Cart {self.pk}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["cart", "product", "variant"], name="unique_cart_product_variant")]

    @property
    def unit_price_paisa(self):
        return self.variant.sell_price_paisa if self.variant else self.product.current_price_paisa

    @property
    def subtotal_paisa(self):
        return self.unit_price_paisa * self.quantity
