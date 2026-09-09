from .models import ServiceCategory,BasePageContent,Page,CartItem
from django.db.models import Sum

def menu_categories(request):
    cart_quantity = 0
    if request.user.is_authenticated:
        result = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))
        cart_quantity = result['total'] or 0
    return {
        'menu_categories': ServiceCategory.objects.all(),
        'base':BasePageContent.objects.first(),
        'page':Page.objects.first(),
        'cart_quantity': cart_quantity,
    }

