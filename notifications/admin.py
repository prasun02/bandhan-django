from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("channel", "subject", "user", "sent_at", "created_at")
    search_fields = ("subject", "body", "user__email")
