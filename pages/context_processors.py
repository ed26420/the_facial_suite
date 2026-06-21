from .models import ServiceCategory

def menu_categories(request):
    return {
        'menu_categories': ServiceCategory.objects.all()
    }

