from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from cart.services import cart_totals
from catalog.models import InventoryMovement, Product, ProductVariant
from payments.adapters import CashOnDeliveryAdapter
from payments.models import Payment
from promotions.services import discount_for

from .models import Order, OrderAddress, OrderItem, OrderSequence, OrderStatusHistory


@transaction.atomic
def next_order_number():
    year = timezone.now().year
    sequence, _ = OrderSequence.objects.select_for_update().get_or_create(year=year)
    sequence.last_number += 1
    sequence.save(update_fields=["last_number"])
    return f"ORD-{year}-{sequence.last_number:06d}"


def reduce_stock_once(order):
    if order.stock_reduced_at:
        return
    for item in order.items.all():
        if item.variant_id_snapshot:
            variant = ProductVariant.objects.select_for_update().get(pk=item.variant_id_snapshot)
            previous = variant.stock
            if previous < item.quantity:
                raise ValidationError("Insufficient stock while placing order.")
            variant.stock -= item.quantity
            variant.save(update_fields=["stock", "updated_at"])
            InventoryMovement.objects.create(product=variant.product, variant=variant, quantity_change=-item.quantity, previous_stock=previous, new_stock=variant.stock, reason=InventoryMovement.Reason.ORDER_PLACED, related_order=order.number)
        else:
            product = Product.objects.select_for_update().get(pk=item.product_id_snapshot)
            previous = product.stock
            if previous < item.quantity:
                raise ValidationError("Insufficient stock while placing order.")
            product.stock -= item.quantity
            product.save(update_fields=["stock", "updated_at"])
            InventoryMovement.objects.create(product=product, quantity_change=-item.quantity, previous_stock=previous, new_stock=product.stock, reason=InventoryMovement.Reason.ORDER_PLACED, related_order=order.number)
    order.stock_reduced_at = timezone.now()
    order.save(update_fields=["stock_reduced_at", "updated_at"])


@transaction.atomic
def create_cod_order(cart, address_snapshot, delivery_zone, user=None, email="", idempotency_token=""):
    if not idempotency_token:
        raise ValidationError("Missing checkout token.")
    existing = Order.objects.filter(idempotency_token=idempotency_token).first()
    if existing:
        return existing
    totals = cart_totals(cart)
    if not totals["items"]:
        raise ValidationError("Cart is empty.")
    delivery_charge = delivery_zone.charge_for(totals["subtotal_paisa"])
    discount = 0
    if cart.coupon:
        discount, free_delivery = discount_for(cart.coupon, totals["subtotal_paisa"], delivery_charge)
        if free_delivery:
            delivery_charge = 0
    grand_total = max(totals["subtotal_paisa"] + delivery_charge - discount, 0)
    order = Order.objects.create(
        number=next_order_number(),
        user=user if user and user.is_authenticated else None,
        email=email,
        phone=address_snapshot["phone"],
        subtotal_paisa=totals["subtotal_paisa"],
        discount_paisa=discount,
        delivery_charge_paisa=delivery_charge,
        grand_total_paisa=grand_total,
        coupon_code=cart.coupon.code if cart.coupon else "",
        delivery_zone_name=delivery_zone.name,
        estimated_delivery=delivery_zone.delivery_estimate,
        idempotency_token=idempotency_token,
    )
    OrderAddress.objects.create(order=order, **address_snapshot)
    for item in totals["items"]:
        OrderItem.objects.create(
            order=order,
            product_id_snapshot=item.product_id,
            variant_id_snapshot=item.variant_id,
            product_name=item.product.name,
            sku=item.variant.sku if item.variant else item.product.sku,
            variant_label=str(item.variant or ""),
            size=item.variant.size if item.variant else "",
            colour=item.variant.colour if item.variant else "",
            unit_price_paisa=item.unit_price_paisa,
            quantity=item.quantity,
            image_reference=(item.product.images.first().image.name if item.product.images.exists() else ""),
        )
    reduce_stock_once(order)
    payment = Payment.objects.create(order=order, method=Payment.Method.COD, status=Payment.Status.COD_PENDING, amount_paisa=grand_total)
    CashOnDeliveryAdapter().create_attempt(payment)
    OrderStatusHistory.objects.create(order=order, status=order.status, note="Order placed with Cash on Delivery.")
    cart.items.all().delete()
    cart.coupon = None
    cart.save(update_fields=["coupon", "updated_at"])
    return order
