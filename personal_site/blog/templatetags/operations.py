from django import template

register = template.Library()

@register.filter
def minus(value, arg):
    """Subtract the arg from the value."""
    return value - arg


