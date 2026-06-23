from django.contrib import admin

from .models import Review, ReviewImage


@admin.action(description="Approve selected reviews")
def approve_reviews(modeladmin, request, queryset):
    queryset.update(status=Review.Status.APPROVED)


@admin.action(description="Reject selected reviews")
def reject_reviews(modeladmin, request, queryset):
    queryset.update(status=Review.Status.REJECTED)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "rating", "title", "status", "is_verified_purchase", "created_at")
    list_filter = ("status", "rating", "is_verified_purchase")
    search_fields = ("product__name", "title", "text", "user__email")
    actions = (approve_reviews, reject_reviews)


admin.site.register(ReviewImage)
