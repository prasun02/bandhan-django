from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Product

from .models import Review


def submit_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_published=True)
    if request.method == "POST":
        Review.objects.create(
            product=product,
            user=request.user if request.user.is_authenticated else None,
            rating=int(request.POST.get("rating", 5)),
            title=request.POST.get("title", ""),
            text=request.POST.get("text", ""),
        )
        messages.success(request, "Review submitted for moderation.")
    template = "partials/reviews.html" if request.headers.get("HX-Request") else "catalog/product_detail.html"
    return render(request, template, {"product": product}) if request.headers.get("HX-Request") else redirect(product.get_absolute_url())
