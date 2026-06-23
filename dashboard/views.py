from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from orders.models import Order


@staff_member_required
def index(request):
    return render(request, "dashboard/index.html", {"recent_orders": Order.objects.order_by("-created_at")[:10]})
