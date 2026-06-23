# CSV Import

The primary import file is `data/imports/bandhan_demo_products_full_details.csv`.

```powershell
python manage.py import_demo_products
python manage.py import_demo_products --path data/imports/custom.csv
```

The importer handles UTF-8 BOM, validates required headers, and uses upsert behavior for products, categories, collections, brands, and variants.
