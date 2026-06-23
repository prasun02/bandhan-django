from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from promotions.services import validate_coupon

from .models import CartItem
from .services import add_item, cart_totals, get_cart, stock_for


def cart_detail(request):
    cart = get_cart(request)
    return render(request, "cart/detail.html", {"cart": cart, **cart_totals(cart)})


def add_to_cart(request):
    cart = get_cart(request)
    try:
        add_item(cart, request.POST.get("product_id"), request.POST.get("variant_id") or None, request.POST.get("quantity", 1))
        messages.success(request, "Added to cart.")
    except ValidationError as exc:
        messages.error(request, exc.message)
    if request.headers.get("HX-Request"):
        return render(request, "partials/cart_summary.html", {"cart": cart, **cart_totals(cart)})
    return redirect("cart:detail")


def buy_now(request):
    response = add_to_cart(request)
    response = redirect("cart:detail")
    if request.headers.get("HX-Request"):
        response["HX-Redirect"] = response.url
    return response


def update_item(request, item_id, action):
    item = get_object_or_404(CartItem, pk=item_id, cart=get_cart(request))
    if action == "increase":
        if item.quantity + 1 > stock_for(item.product, item.variant):
            messages.error(request, "Requested quantity is not available.")
        else:
            item.quantity += 1
            item.save(update_fields=["quantity", "updated_at"])
    elif action == "decrease" and item.quantity > 1:
        item.quantity -= 1
        item.save(update_fields=["quantity", "updated_at"])
    elif action == "remove":
        item.delete()
    cart = get_cart(request)
    template = "partials/cart_summary.html" if request.headers.get("HX-Request") else "cart/detail.html"
    return render(request, template, {"cart": cart, **cart_totals(cart)})


def apply_coupon(request):
    cart = get_cart(request)
    totals = cart_totals(cart)
    try:
        cart.coupon = validate_coupon(request.POST.get("code", ""), totals["subtotal_paisa"], request.user)
        cart.save(update_fields=["coupon", "updated_at"])
        messages.success(request, "Coupon applied.")
    except ValidationError as exc:
        messages.error(request, exc.message)
    return render(request, "partials/cart_summary.html", {"cart": cart, **cart_totals(cart)})
