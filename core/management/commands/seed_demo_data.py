from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from promotions.models import Coupon
from shipping.models import DeliveryZone


class Command(BaseCommand):
    help = "Seed idempotent delivery zones and demo coupons."

    def handle(self, *args, **options):
        DeliveryZone.objects.update_or_create(slug="inside-dhaka", defaults={"name": "Inside Dhaka", "charge_paisa": 8000, "free_delivery_threshold_paisa": 500000, "delivery_estimate": "1-2 business days", "districts": "Dhaka"})
        DeliveryZone.objects.update_or_create(slug="outside-dhaka", defaults={"name": "Outside Dhaka", "charge_paisa": 15000, "free_delivery_threshold_paisa": 800000, "delivery_estimate": "2-4 business days"})
        DeliveryZone.objects.update_or_create(slug="remote-area", defaults={"name": "Remote Area", "charge_paisa": 20000, "free_delivery_threshold_paisa": None, "delivery_estimate": "3-6 business days"})
        start = timezone.now() - timedelta(days=1)
        end = timezone.now() + timedelta(days=365)
        Coupon.objects.update_or_create(code="WELCOME10", defaults={"discount_type": Coupon.DiscountType.PERCENTAGE, "value": 10, "minimum_order_paisa": 150000, "maximum_discount_paisa": 50000, "start_at": start, "end_at": end, "is_active": True})
        Coupon.objects.update_or_create(code="PUJA500", defaults={"discount_type": Coupon.DiscountType.FIXED, "value": 500, "minimum_order_paisa": 500000, "start_at": start, "end_at": end, "is_active": True})
        Coupon.objects.update_or_create(code="FREEDHAKA", defaults={"discount_type": Coupon.DiscountType.FREE_DELIVERY, "value": 0, "minimum_order_paisa": 300000, "start_at": start, "end_at": end, "is_active": True})
        self.stdout.write(self.style.SUCCESS("Seeded delivery zones and coupons."))
