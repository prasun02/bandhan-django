from django.core.exceptions import ValidationError
from django.db.models import Count

from .models import Coupon, CouponRedemption


def validate_coupon(code, subtotal_paisa, user=None):
    coupon = Coupon.objects.filter(code__iexact=code.strip()).first()
    if not coupon or not coupon.is_valid_now():
        raise ValidationError("Coupon is not active.")
    if subtotal_paisa < coupon.minimum_order_paisa:
        raise ValidationError("Order does not meet the coupon minimum.")
    if coupon.usage_limit and coupon.redemptions.count() >= coupon.usage_limit:
        raise ValidationError("Coupon usage limit has been reached.")
    if user and user.is_authenticated:
        used = CouponRedemption.objects.filter(coupon=coupon, user=user).aggregate(total=Count("id"))["total"]
        if used >= coupon.per_customer_limit:
            raise ValidationError("Coupon has already been used by this account.")
    return coupon


def discount_for(coupon, subtotal_paisa, delivery_charge_paisa=0):
    if not coupon:
        return 0, False
    if coupon.discount_type == Coupon.DiscountType.FREE_DELIVERY:
        return delivery_charge_paisa, True
    if coupon.discount_type == Coupon.DiscountType.FIXED:
        discount = min(coupon.value * 100, subtotal_paisa)
    else:
        discount = subtotal_paisa * coupon.value // 100
    if coupon.maximum_discount_paisa:
        discount = min(discount, coupon.maximum_discount_paisa)
    return discount, False
