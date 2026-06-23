from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from catalog.importers import import_products


class Command(BaseCommand):
    help = "Import Bandhan demo products from CSV files idempotently."

    def add_arguments(self, parser):
        parser.add_argument("--path", default=None)

    def handle(self, *args, **options):
        default = settings.BASE_DIR / "data" / "imports" / "bandhan_demo_products_full_details.csv"
        fallback = settings.BASE_DIR / "data" / "imports" / "bandhan_demo_products_import.csv"
        path = Path(options["path"] or (default if default.exists() else fallback))
        stats = import_products(path)
        for key, value in stats.items():
            self.stdout.write(f"{key}: {value}")
