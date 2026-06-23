from django.db import models


class SiteSetting(models.Model):
    key = models.CharField(max_length=80, unique=True)
    value = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key


class Banner(models.Model):
    title = models.CharField(max_length=160)
    subtitle = models.CharField(max_length=220, blank=True)
    image = models.ImageField(upload_to="banners/", blank=True)
    link_url = models.CharField(max_length=240, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "title")

    def __str__(self):
        return self.title
