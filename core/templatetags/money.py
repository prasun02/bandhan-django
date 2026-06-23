from django import template

from core.money import money as format_money

register = template.Library()


@register.filter(name="money")
def money(value):
    return format_money(value)
