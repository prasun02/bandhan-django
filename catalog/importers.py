import csv
from pathlib import Path

from django.db import transaction
from django.utils.text import slugify

from core.money import taka_to_paisa

from .models import Brand, Category, Collection, InventoryMovement, Product, ProductVariant

EXPECTED_HEADERS = {"name", "sku", "category", "regular_price", "stock"}


def truthy(value):
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


@transaction.atomic
def import_products(path):
    stats = {"rows_read": 0, "products_created": 0, "products_updated": 0, "products_skipped": 0, "images_created": 0, "variants_created": 0, "validation_errors": []}
    path = Path(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        missing = EXPECTED_HEADERS - headers
        if missing:
            raise ValueError(f"Missing CSV headers: {', '.join(sorted(missing))}")
        for row_number, row in enumerate(reader, start=2):
            stats["rows_read"] += 1
            if not row.get("name") or not row.get("sku"):
                stats["products_skipped"] += 1
                stats["validation_errors"].append(f"Row {row_number}: missing name or sku")
                continue
            category, _ = Category.objects.get_or_create(name=row["category"].strip(), defaults={"slug": slugify(row["category"])})
            brand = None
            if row.get("brand"):
                brand, _ = Brand.objects.get_or_create(name=row["brand"].strip(), defaults={"slug": slugify(row["brand"])})
            product, created = Product.objects.update_or_create(
                sku=row["sku"].strip(),
                defaults={
                    "name": row["name"].strip(),
                    "slug": row.get("slug") or slugify(row["name"]),
                    "category": category,
                    "brand": brand,
                    "short_description": row.get("short_description", ""),
                    "full_description": row.get("full_description", ""),
                    "fabric": row.get("fabric", ""),
                    "occasion": row.get("occasion", ""),
                    "stitching_type": row.get("stitching_type", ""),
                    "regular_price_paisa": taka_to_paisa(row["regular_price"]),
                    "sale_price_paisa": taka_to_paisa(row["sale_price"]) if row.get("sale_price") else None,
                    "stock": int(row.get("stock") or 0),
                    "is_published": truthy(row.get("is_published", "true")),
                    "is_featured": truthy(row.get("is_featured")),
                    "is_new_arrival": truthy(row.get("is_new_arrival")),
                    "is_best_seller": truthy(row.get("is_best_seller")),
                    "is_sale": truthy(row.get("is_sale")),
                    "seo_title": row.get("seo_title", ""),
                    "seo_description": row.get("seo_description", ""),
                },
            )
            stats["products_created" if created else "products_updated"] += 1
            for collection_name in [item.strip() for item in row.get("collections", "").split("|") if item.strip()]:
                collection, _ = Collection.objects.get_or_create(name=collection_name, defaults={"slug": slugify(collection_name)})
                product.collections.add(collection)
            if row.get("variant_sku"):
                variant, variant_created = ProductVariant.objects.update_or_create(
                    sku=row["variant_sku"].strip(),
                    defaults={"product": product, "size": row.get("size", ""), "colour": row.get("colour", ""), "stock": int(row.get("variant_stock") or row.get("stock") or 0)},
                )
                if variant_created:
                    stats["variants_created"] += 1
                    InventoryMovement.objects.create(product=product, variant=variant, quantity_change=variant.stock, previous_stock=0, new_stock=variant.stock, reason=InventoryMovement.Reason.INITIAL_IMPORT, note="CSV import")
    return stats
