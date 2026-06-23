from django.db import models


class DeliveryZone(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    charge_paisa = models.PositiveBigIntegerField()
    free_delivery_threshold_paisa = models.PositiveBigIntegerField(null=True, blank=True)
    delivery_estimate = models.CharField(max_length=120)
    districts = models.TextField(blank=True, help_text="Comma-separated district names.")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("charge_paisa", "name")

    def __str__(self):
        return self.name

    def charge_for(self, subtotal_paisa):
        if self.free_delivery_threshold_paisa and subtotal_paisa >= self.free_delivery_threshold_paisa:
            return 0
        return self.charge_paisa
