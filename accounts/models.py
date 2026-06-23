from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        STAFF = "staff", "Staff"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32, blank=True)
    full_name = models.CharField(max_length=160)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    email_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.email


class CustomerProfile(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    alternative_phone = models.CharField(max_length=32, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    marketing_consent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.full_name or self.user.email


class Address(models.Model):
    class Label(models.TextChoices):
        HOME = "home", "Home"
        OFFICE = "office", "Office"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=160)
    phone = models.CharField(max_length=32)
    alternative_phone = models.CharField(max_length=32, blank=True)
    division = models.CharField(max_length=80)
    district = models.CharField(max_length=80)
    upazila = models.CharField(max_length=80, verbose_name="Upazila or Thana")
    area = models.CharField(max_length=120)
    road = models.CharField(max_length=160, verbose_name="Road, village, or street")
    house = models.CharField(max_length=80, blank=True, verbose_name="House or holding number")
    postal_code = models.CharField(max_length=20, blank=True)
    landmark = models.CharField(max_length=160, blank=True)
    delivery_instructions = models.TextField(blank=True)
    label = models.CharField(max_length=20, choices=Label.choices, default=Label.HOME)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["user", "is_default"])]

    def __str__(self):
        return f"{self.full_name}, {self.district}"

    def as_snapshot(self):
        return {
            "full_name": self.full_name,
            "phone": self.phone,
            "alternative_phone": self.alternative_phone,
            "division": self.division,
            "district": self.district,
            "upazila": self.upazila,
            "area": self.area,
            "road": self.road,
            "house": self.house,
            "postal_code": self.postal_code,
            "landmark": self.landmark,
            "delivery_instructions": self.delivery_instructions,
            "label": self.label,
        }
