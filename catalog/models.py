from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:category", args=[self.slug])


class Collection(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="collections/", blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=210, unique=True)
    sku = models.CharField(max_length=80, unique=True)
    short_description = models.CharField(max_length=260, blank=True)
    full_description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    collections = models.ManyToManyField(Collection, blank=True, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products", null=True, blank=True)
    fabric = models.CharField(max_length=120, blank=True)
    occasion = models.CharField(max_length=120, blank=True)
    stitching_type = models.CharField(max_length=120, blank=True)
    regular_price_paisa = models.PositiveBigIntegerField(validators=[MinValueValidator(0)])
    sale_price_paisa = models.PositiveBigIntegerField(null=True, blank=True)
    cost_price_paisa = models.PositiveBigIntegerField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=3)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=False)
    is_return_eligible = models.BooleanField(default=True)
    care_instructions = models.TextField(blank=True)
    package_contents = models.TextField(blank=True)
    estimated_delivery = models.CharField(max_length=160, blank=True)
    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.CharField(max_length=260, blank=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_published", "is_archived"]),
            models.Index(fields=["is_featured", "is_new_arrival", "is_best_seller"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product_detail", args=[self.slug])

    @property
    def current_price_paisa(self):
        return self.sale_price_paisa or self.regular_price_paisa


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=180)
    display_order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    gallery_key = models.CharField(max_length=220)

    class Meta:
        ordering = ("display_order", "id")
        constraints = [models.UniqueConstraint(fields=["product", "gallery_key"], name="unique_product_gallery_key")]

    def save(self, *args, **kwargs):
        if not self.gallery_key:
            self.gallery_key = f"{self.product_id}-{self.image.name}"
        super().save(*args, **kwargs)


class ProductVariant(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    sku = models.CharField(max_length=90, unique=True)
    size = models.CharField(max_length=40, blank=True)
    colour = models.CharField(max_length=60, blank=True)
    price_override_paisa = models.PositiveBigIntegerField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    reserved_stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    image = models.ForeignKey(ProductImage, on_delete=models.SET_NULL, null=True, blank=True)
    weight_grams = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["product", "size", "colour"], name="unique_product_size_colour")]
        indexes = [models.Index(fields=["product", "is_active"])]

    def __str__(self):
        return f"{self.product.name} - {self.size} / {self.colour}".strip()

    @property
    def sell_price_paisa(self):
        return self.price_override_paisa or self.product.current_price_paisa

    @property
    def available_stock(self):
        return max(self.stock - self.reserved_stock, 0)


class ProductAttribute(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attribute_values")
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=160)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["product", "attribute", "value"], name="unique_product_attribute_value")]


class InventoryMovement(models.Model):
    class Reason(models.TextChoices):
        INITIAL_IMPORT = "initial_import", "Initial import"
        MANUAL_ADJUSTMENT = "manual_adjustment", "Manual adjustment"
        ORDER_PLACED = "order_placed", "Order placed"
        ORDER_CANCELLED = "order_cancelled", "Order cancelled"
        RETURN_APPROVED = "return_approved", "Return approved"
        RESTOCKING = "restocking", "Restocking"
        DAMAGED = "damaged", "Damaged item"
        ADMIN_CORRECTION = "admin_correction", "Administrative correction"

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, null=True, blank=True)
    quantity_change = models.IntegerField()
    previous_stock = models.IntegerField()
    new_stock = models.IntegerField()
    reason = models.CharField(max_length=40, choices=Reason.choices)
    related_order = models.CharField(max_length=40, blank=True)
    staff_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ("-timestamp",)


class RelatedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="related_links")
    related_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="+")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["product", "related_product"], name="unique_related_product")]


class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist")
    created_at = models.DateTimeField(auto_now_add=True)


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["wishlist", "product"], name="unique_wishlist_product")]


class RecentlyViewedProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=80, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)
