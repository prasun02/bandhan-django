from django.db.models import Count, Q

from .models import Category, Collection, Product


def published_products():
    return Product.objects.filter(is_published=True, is_archived=False).select_related("category", "brand").prefetch_related("images", "variants", "collections")


def home_products():
    products = published_products()
    return {
        "featured_categories": Category.objects.filter(is_active=True).annotate(product_count=Count("products")).order_by("name")[:8],
        "new_arrivals": products.filter(is_new_arrival=True)[:8],
        "best_sellers": products.filter(is_best_seller=True)[:8],
        "sarees": products.filter(category__slug__icontains="saree")[:8],
        "salwar": products.filter(category__slug__icontains="salwar")[:8],
        "bridal": products.filter(Q(collections__slug__icontains="bridal") | Q(category__slug__icontains="bridal")).distinct()[:8],
    }


def search_products(query):
    products = published_products()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(sku__icontains=query) | Q(short_description__icontains=query))
    return products
