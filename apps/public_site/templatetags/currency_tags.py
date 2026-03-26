from django import template

register = template.Library()

_CURRENCY_SYMBOLS: dict[str, str] = {
    "ILS": "₪",
    "USD": "$",
    "EUR": "€",
}


@register.filter
def currency_symbol(iso_code: str) -> str:
    """Map a currency ISO code to its symbol. Falls back to the code itself."""
    return _CURRENCY_SYMBOLS.get(iso_code, iso_code)
