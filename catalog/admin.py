from django.contrib import admin

from .models import (
    AttributeValue,
    Brand,
    Category,
    Collection,
    InventoryMovement,
    Product,
    ProductAttribute,
    ProductImage,
    ProductVariant,
    RecentlyViewedProduct,
    RelatedProduct,
    Wishlist,
    WishlistItem,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.action(description="Publish selected products")
def publish_products(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description="Unpublish selected products")
def unpublish_products(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "regular_price_paisa", "sale_price_paisa", "stock", "is_published", "is_featured")
    list_filter = ("category", "collections", "is_published", "is_featured", "is_new_arrival", "is_best_seller", "is_sale")
    search_fields = ("name", "sku", "slug")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category", "brand")
    filter_horizontal = ("collections",)
    inlines = (ProductImageInline, ProductVariantInline)
    actions = (publish_products, unpublish_products)
    date_hierarchy = "created_at"


@admin.register(Category, Collection, Brand)
class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(ProductAttribute)
admin.site.register(AttributeValue)
admin.site.register(InventoryMovement)
admin.site.register(RelatedProduct)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(RecentlyViewedProduct)
