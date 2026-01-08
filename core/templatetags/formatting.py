# <tu_app>/templatetags/formatting.py
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from django import template

register = template.Library()

def _to_decimal(value):
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None

@register.filter
def num(value, decimals=2):
    """
    1234.5 -> 1.234,50
    """
    d = _to_decimal(value)
    if d is None:
        return value

    try:
        decimals = int(decimals)
    except (ValueError, TypeError):
        decimals = 2

    q = Decimal(10) ** -decimals
    d = d.quantize(q, rounding=ROUND_HALF_UP)

    s = f"{d:,.{decimals}f}"          # 1,234.50
    return s.replace(",", "X").replace(".", ",").replace("X", ".")  # 1.234,50
