from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from config.settings.base import env


class Command(BaseCommand):
    help = "Create or update a deployment superuser from environment variables."

    def handle(self, *args, **options):
        email = env("DJANGO_SUPERUSER_EMAIL", "").strip().lower()
        password = env("DJANGO_SUPERUSER_PASSWORD", "")
        full_name = env("DJANGO_SUPERUSER_FULL_NAME", "Bandhan Admin").strip()

        if not email or not password:
            raise CommandError("DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD are required.")

        User = get_user_model()
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "full_name": full_name,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "role": "admin",
            },
        )
        changed = False
        if created:
            user.set_password(password)
            changed = True
        for field, value in {
            "full_name": full_name,
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
            "role": "admin",
        }.items():
            if getattr(user, field) != value:
                setattr(user, field, value)
                changed = True
        if changed:
            user.save()
        self.stdout.write(self.style.SUCCESS("Superuser ensured."))
