from decimal import Decimal, ROUND_HALF_UP

from django import template
from django.conf import settings

register = template.Library()


def taka_to_paisa(value):
    return int((Decimal(str(value)) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def paisa_to_taka(value):
    return Decimal(value or 0) / Decimal("100")


@register.filter
def money(value):
    return f"{settings.BANDHAN_CURRENCY_SYMBOL}{paisa_to_taka(value):,.0f}"
