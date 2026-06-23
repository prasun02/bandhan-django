from django.conf import settings


def brand(request):
    return {
        "BRAND_NAME": "Bandhan",
        "BRAND_TAGLINE": "Tradition Woven with Elegance",
        "CONTACT_PHONE": settings.BANDHAN_CONTACT_PHONE,
    }
