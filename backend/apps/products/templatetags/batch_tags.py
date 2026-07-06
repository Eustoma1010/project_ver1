from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Trừ hai số: {{ value|subtract:arg }}"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0
