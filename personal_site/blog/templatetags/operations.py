from django import template
import datetime

register = template.Library()

@register.filter
def minus(value, arg):
    """Subtract the arg from the value."""
    return value - arg

@register.filter
def minus_date(current_date, date_to_subtract):
    """
        substract date_to_subtract from current_date and return the difference in years and months.
        date is presented as '2024-06-21' string.
    """

    date_parts = [int(part) for part in date_to_subtract.split('-')]
    date_to_subtract_obj = datetime.date(date_parts[0], date_parts[1], date_parts[2])
    delta = current_date - date_to_subtract_obj
    total_months = delta.days // 30  # Approximate number of months
    years = total_months // 12
    months = total_months % 12

    response = ""

    if years == 1:
        response += f"{years} rok "
    elif years > 1:
        response += f"{years} roky "
    if months == 1:
        response += f"{months} měsíc"
    elif months == 2 or months == 3 or months == 4:
        response += f"{months} měsíce"
    elif months >= 5:
        response += f"{months} měsíců"
    return response.strip()