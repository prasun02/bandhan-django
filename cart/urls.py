from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path("add/", views.add_to_cart, name="add"),
    path("buy-now/", views.buy_now, name="buy_now"),
    path("item/<int:item_id>/<str:action>/", views.update_item, name="update_item"),
    path("coupon/", views.apply_coupon, name="apply_coupon"),
]
