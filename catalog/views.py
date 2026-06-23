from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Collection, Product, Wishlist, WishlistItem
from .selectors import published_products, search_products


def shop(request):
    products = search_products(request.GET.get("q"))
    category = request.GET.get("category")
    if category:
        products = products.filter(category__slug=category)
    context = {
        "products": products,
        "categories": Category.objects.filter(is_active=True).annotate(product_count=Count("products")),
        "query": request.GET.get("q", ""),
    }
    template = "partials/product_grid.html" if request.headers.get("HX-Request") else "catalog/shop.html"
    return render(request, template, context)


def product_detail(request, slug):
    product = get_object_or_404(published_products(), slug=slug)
    return render(request, "catalog/product_detail.html", {"product": product, "related_products": published_products().exclude(pk=product.pk)[:4]})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    return render(request, "catalog/category.html", {"category": category, "products": published_products().filter(category=category)})


def collection_detail(request, slug):
    collection = get_object_or_404(Collection, slug=slug, is_active=True)
    return render(request, "catalog/collection.html", {"collection": collection, "products": published_products().filter(collections=collection)})


def flagged(request, flag):
    mapping = {
        "new-arrivals": {"is_new_arrival": True},
        "best-sellers": {"is_best_seller": True},
        "sale": {"is_sale": True},
        "puja-collection": {"collections__slug__icontains": "puja"},
    }
    return render(request, "catalog/shop.html", {"products": published_products().filter(**mapping[flag]), "query": ""})


def search_suggestions(request):
    products = search_products(request.GET.get("q", ""))[:8]
    return render(request, "partials/search_suggestions.html", {"products": products})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    if not created:
        item.delete()
    if request.headers.get("HX-Request"):
        return render(request, "partials/wishlist_button.html", {"product": product, "in_wishlist": created})
    return redirect(product.get_absolute_url())
