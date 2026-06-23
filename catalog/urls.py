from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("shop/", views.shop, name="shop"),
    path("search-suggestions/", views.search_suggestions, name="search_suggestions"),
    path("new-arrivals/", views.flagged, {"flag": "new-arrivals"}, name="new_arrivals"),
    path("best-sellers/", views.flagged, {"flag": "best-sellers"}, name="best_sellers"),
    path("sale/", views.flagged, {"flag": "sale"}, name="sale"),
    path("puja-collection/", views.flagged, {"flag": "puja-collection"}, name="puja_collection"),
    path("category/<slug:slug>/", views.category_detail, name="category"),
    path("collection/<slug:slug>/", views.collection_detail, name="collection"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("wishlist/<int:product_id>/toggle/", views.toggle_wishlist, name="toggle_wishlist"),
]
