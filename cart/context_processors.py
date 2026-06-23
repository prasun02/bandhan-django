from .services import get_cart


def cart_summary(request):
    try:
        cart = get_cart(request)
        count = sum(item.quantity for item in cart.items.all())
    except Exception:
        count = 0
    return {"cart_quantity": count}
