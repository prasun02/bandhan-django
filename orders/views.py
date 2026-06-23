from django.shortcuts import render

from .models import Order


def track_order(request):
    order = None
    if request.method == "POST":
        order = Order.objects.filter(number=request.POST.get("order_number", "").strip(), phone=request.POST.get("phone", "").strip()).prefetch_related("history").first()
    return render(request, "orders/track.html", {"order": order})
