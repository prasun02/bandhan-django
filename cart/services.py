import uuid

from django.core.exceptions import ValidationError
from django.db import transaction

from catalog.models import Product, ProductVariant

from .models import Cart, CartItem

CART_SESSION_KEY = "bandhan_cart_id"


def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    cart_id = request.session.get(CART_SESSION_KEY)
    if cart_id:
        cart = Cart.objects.filter(session_key=cart_id, user__isnull=True).first()
        if cart:
            return cart
    cart = Cart.objects.create(session_key=uuid.uuid4())
    request.session[CART_SESSION_KEY] = str(cart.session_key)
    return cart


def merge_session_cart(request, user):
    session_id = request.session.get(CART_SESSION_KEY)
    if not session_id:
        return
    guest = Cart.objects.filter(session_key=session_id, user__isnull=True).first()
    if not guest:
        return
    customer_cart, _ = Cart.objects.get_or_create(user=user)
    for item in guest.items.select_related("product", "variant"):
        target, created = CartItem.objects.get_or_create(cart=customer_cart, product=item.product, variant=item.variant, defaults={"quantity": item.quantity})
        if not created:
            target.quantity += item.quantity
            target.save(update_fields=["quantity", "updated_at"])
    guest.delete()
    request.session.pop(CART_SESSION_KEY, None)


def stock_for(product, variant=None):
    return variant.available_stock if variant else product.stock


@transaction.atomic
def add_item(cart, product_id, variant_id=None, quantity=1):
    product = Product.objects.select_for_update().get(pk=product_id, is_published=True, is_archived=False)
    variant = None
    if product.variants.exists():
        if not variant_id:
            raise ValidationError("Please select size and colour.")
        variant = ProductVariant.objects.select_for_update().get(pk=variant_id, product=product, is_active=True)
    quantity = max(int(quantity or 1), 1)
    available = stock_for(product, variant)
    item, created = CartItem.objects.select_for_update().get_or_create(cart=cart, product=product, variant=variant, defaults={"quantity": 0})
    if item.quantity + quantity > available:
        raise ValidationError("Requested quantity is not available.")
    item.quantity += quantity
    item.save(update_fields=["quantity", "updated_at"])
    return item


def cart_totals(cart):
    items = cart.items.select_related("product", "variant").prefetch_related("product__images")
    subtotal = sum(item.subtotal_paisa for item in items)
    return {"items": items, "subtotal_paisa": subtotal, "total_quantity": sum(item.quantity for item in items)}
