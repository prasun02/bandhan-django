from pathlib import Path
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core import management
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse

from cart.models import Cart
from cart.services import add_item
from catalog.importers import import_products
from catalog.models import Category, Product, ProductVariant
from orders.services import create_cod_order
from promotions.models import Coupon
from promotions.services import discount_for, validate_coupon
from shipping.models import DeliveryZone


class CommerceFlowTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Sarees", slug="sarees")
        self.product = Product.objects.create(name="Test Saree", slug="test-saree", sku="TS-1", category=self.category, regular_price_paisa=100000, stock=5, is_published=True)
        self.variant = ProductVariant.objects.create(product=self.product, sku="TS-1-M-RED", size="M", colour="Red", stock=5)
        self.zone = DeliveryZone.objects.create(name="Inside Dhaka", slug="inside-dhaka", charge_paisa=8000, free_delivery_threshold_paisa=500000, delivery_estimate="1-2 business days")

    def test_homepage_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_respects_variant_stock(self):
        cart = Cart.objects.create()
        item = add_item(cart, self.product.id, self.variant.id, 2)
        self.assertEqual(item.quantity, 2)

    def test_add_to_cart_rejects_stock_overrun(self):
        cart = Cart.objects.create()
        with self.assertRaises(ValidationError):
            add_item(cart, self.product.id, self.variant.id, 99)

    def test_cod_order_reduces_stock_once_and_is_idempotent(self):
        cart = Cart.objects.create()
        add_item(cart, self.product.id, self.variant.id, 2)
        snapshot = {"full_name": "A Customer", "phone": "01700000000", "alternative_phone": "", "division": "Dhaka", "district": "Dhaka", "upazila": "Dhanmondi", "area": "Area", "road": "Road", "house": "", "postal_code": "", "landmark": "", "delivery_instructions": "", "label": "home"}
        order = create_cod_order(cart, snapshot, self.zone, idempotency_token="once")
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock, 3)
        same_order = create_cod_order(cart, snapshot, self.zone, idempotency_token="once")
        self.assertEqual(order.pk, same_order.pk)
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock, 3)

    def test_checkout_page_requires_cart_items(self):
        response = self.client.get(reverse("checkout:checkout"))
        self.assertRedirects(response, reverse("cart:detail"))

    def test_product_detail_and_shop_load(self):
        self.assertEqual(self.client.get(reverse("catalog:shop")).status_code, 200)
        self.assertEqual(self.client.get(self.product.get_absolute_url()).status_code, 200)

    def test_coupon_validation_and_delivery_discount(self):
        from django.utils import timezone
        from datetime import timedelta

        coupon = Coupon.objects.create(
            code="TEST10",
            discount_type=Coupon.DiscountType.PERCENTAGE,
            value=10,
            minimum_order_paisa=50000,
            maximum_discount_paisa=20000,
            start_at=timezone.now() - timedelta(days=1),
            end_at=timezone.now() + timedelta(days=1),
        )
        self.assertEqual(validate_coupon("TEST10", 100000), coupon)
        self.assertEqual(discount_for(coupon, 100000)[0], 10000)

    def test_registration_and_login(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "full_name": "Test Customer",
                "email": "customer@example.com",
                "phone": "01700000000",
                "password1": "StrongPass12345",
                "password2": "StrongPass12345",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        logged_in = self.client.login(email="customer@example.com", password="StrongPass12345")
        self.assertTrue(logged_in)

    def test_csv_importer_is_idempotent(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "products.csv"
            path.write_text(
                "name,sku,category,regular_price,stock\nImported Saree,IMP-1,Sarees,1200,4\n",
                encoding="utf-8",
            )
            first = import_products(path)
            second = import_products(path)
        self.assertEqual(first["products_created"], 1)
        self.assertEqual(second["products_created"], 0)
        self.assertEqual(second["products_updated"], 1)

    @override_settings(DJANGO_SUPERUSER_EMAIL="admin@example.com")
    def test_ensure_superuser_command(self):
        with self.settings():
            import os

            os.environ["DJANGO_SUPERUSER_EMAIL"] = "admin@example.com"
            os.environ["DJANGO_SUPERUSER_PASSWORD"] = "StrongAdmin12345"
            os.environ["DJANGO_SUPERUSER_FULL_NAME"] = "Bandhan Admin"
            management.call_command("ensure_superuser", verbosity=0)
            management.call_command("ensure_superuser", verbosity=0)
            User = get_user_model()
            self.assertEqual(User.objects.filter(email="admin@example.com").count(), 1)
            self.assertTrue(User.objects.get(email="admin@example.com").is_superuser)
