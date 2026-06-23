from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Address, CustomerProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "full_name", "phone", "role", "is_active", "is_staff", "date_joined")
    list_filter = ("role", "is_active", "is_staff", "email_verified")
    search_fields = ("email", "full_name", "phone")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "phone", "role", "email_verified")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "full_name", "phone", "password1", "password2")}),)


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "marketing_consent", "updated_at")
    search_fields = ("user__email", "user__full_name", "user__phone")
    list_filter = ("status", "marketing_consent")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "district", "upazila", "label", "is_default")
    list_filter = ("division", "district", "label", "is_default")
    search_fields = ("full_name", "phone", "district", "area", "road")
