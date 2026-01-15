from .models import Category

def navbar_context(request):
    """Provide navbar categories to all templates."""
    return {
        'categories': Category.objects.filter(blogpost__is_published=True).distinct()
    }