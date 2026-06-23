from django.conf import settings
from django.db import models


class OrderSequence(models.Model):
    year = models.PositiveIntegerField(unique=True)
    last_number = models.PositiveIntegerField(default=0)


class Order(models.Model):
    class Status(models.TextChoices):
        PLACED = "placed", "Order Placed"
        AWAITING_PAYMENT = "awaiting_payment", "Awaiting Payment"
        PAYMENT_CONFIRMED = "payment_confirmed", "Payment Confirmed"
        CONFIRMED = "confirmed", "Confirmed"
        PROCESSING = "processing", "Processing"
        PACKED = "packed", "Packed"
        READY = "ready_for_shipment", "Ready for Shipment"
        SHIPPED = "shipped", "Shipped"
        OUT_FOR_DELIVERY = "out_for_delivery", "Out for Delivery"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"
        RETURN_REQUESTED = "return_requested", "Return Requested"
        RETURNED = "returned", "Returned"
        REFUND_PROCESSING = "refund_processing", "Refund Processing"
        REFUNDED = "refunded", "Refunded"
        FAILED_DELIVERY = "failed_delivery", "Failed Delivery"

    number = models.CharField(max_length=24, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32)
    status = models.CharField(max_length=40, choices=Status.choices, default=Status.PLACED)
    subtotal_paisa = models.PositiveBigIntegerField()
    discount_paisa = models.PositiveBigIntegerField(default=0)
    delivery_charge_paisa = models.PositiveBigIntegerField(default=0)
    payment_fee_paisa = models.PositiveBigIntegerField(default=0)
    grand_total_paisa = models.PositiveBigIntegerField()
    coupon_code = models.CharField(max_length=40, blank=True)
    delivery_zone_name = models.CharField(max_length=80, blank=True)
    estimated_delivery = models.CharField(max_length=120, blank=True)
    idempotency_token = models.CharField(max_length=120, unique=True)
    stock_reduced_at = models.DateTimeField(null=True, blank=True)
    restocked_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id_snapshot = models.PositiveBigIntegerField()
    variant_id_snapshot = models.PositiveBigIntegerField(null=True, blank=True)
    product_name = models.CharField(max_length=180)
    sku = models.CharField(max_length=90)
    variant_label = models.CharField(max_length=120, blank=True)
    size = models.CharField(max_length=40, blank=True)
    colour = models.CharField(max_length=60, blank=True)
    unit_price_paisa = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField()
    image_reference = models.CharField(max_length=240, blank=True)
    discount_paisa = models.PositiveBigIntegerField(default=0)
    tax_paisa = models.PositiveBigIntegerField(default=0)

    @property
    def subtotal_paisa(self):
        return self.unit_price_paisa * self.quantity


class OrderAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="address")
    full_name = models.CharField(max_length=160)
    phone = models.CharField(max_length=32)
    alternative_phone = models.CharField(max_length=32, blank=True)
    division = models.CharField(max_length=80)
    district = models.CharField(max_length=80)
    upazila = models.CharField(max_length=80)
    area = models.CharField(max_length=120)
    road = models.CharField(max_length=160)
    house = models.CharField(max_length=80, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    landmark = models.CharField(max_length=160, blank=True)
    delivery_instructions = models.TextField(blank=True)
    label = models.CharField(max_length=20, blank=True)


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="history")
    status = models.CharField(max_length=40, choices=Order.Status.choices)
    note = models.TextField(blank=True)
    visible_to_customer = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="shipment")
    courier = models.CharField(max_length=120, blank=True)
    tracking_number = models.CharField(max_length=120, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)


class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="invoice")
    invoice_number = models.CharField(max_length=40, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
