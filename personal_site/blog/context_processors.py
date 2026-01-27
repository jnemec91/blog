from .models import Category
from datetime import datetime

def navbar_context(request):
    """Provide navbar categories to all templates."""
    return {
        'categories': Category.objects.filter(blogpost__is_published=True).distinct()
    }

def current_year(request):
    """Provide the current year to all templates."""
    return {
        'current_year': datetime.now().year
    }