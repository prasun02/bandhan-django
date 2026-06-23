import uuid

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from cart.services import cart_totals, get_cart
from orders.services import create_cod_order
from shipping.models import DeliveryZone

from .forms import GuestCheckoutForm


def checkout(request):
    cart = get_cart(request)
    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart:detail")
    if "checkout_token" not in request.session:
        request.session["checkout_token"] = uuid.uuid4().hex
    zones = DeliveryZone.objects.filter(is_active=True)
    form = GuestCheckoutForm(request.POST or None, zones=zones, initial={"idempotency_token": request.session["checkout_token"], "payment_method": "cod"})
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["payment_method"] != "cod":
            messages.error(request, "Online payment adapters are prepared but require verified provider credentials.")
            return redirect("checkout:checkout")
        zone = get_object_or_404(DeliveryZone, pk=form.cleaned_data["delivery_zone"], is_active=True)
        snapshot = {field: form.cleaned_data[field] for field in ["full_name", "phone", "alternative_phone", "division", "district", "upazila", "area", "road", "house", "postal_code", "landmark", "delivery_instructions", "label"]}
        try:
            order = create_cod_order(cart, snapshot, zone, request.user, form.cleaned_data.get("email", ""), form.cleaned_data["idempotency_token"])
        except ValidationError as exc:
            messages.error(request, exc.message)
        else:
            request.session.pop("checkout_token", None)
            response = redirect("checkout:success", order_number=order.number)
            if request.headers.get("HX-Request"):
                response["HX-Redirect"] = response.url
            return response
    return render(request, "checkout/checkout.html", {"form": form, "cart": cart, "zones": zones, **cart_totals(cart)})


def order_success(request, order_number):
    return render(request, "checkout/success.html", {"order_number": order_number})
