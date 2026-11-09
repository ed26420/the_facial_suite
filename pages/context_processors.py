from .models import ServiceCategory, BasePageContent, Page, CartItem
from django.db.models import Sum

def menu_categories(request):
    cart_quantity = 0
    if request.user.is_authenticated:
        result = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))
        cart_quantity = result['total'] or 0

    # OPTIMIZED: Prefetch related sub-items (treatments/subcategories) rendered in navigation dropdowns.
    # Replace 'treatments' with your model's exact related field name if different.
    categories = ServiceCategory.objects.prefetch_related('treatments').all()

    return {
        'menu_categories': categories,
        'base': BasePageContent.objects.first(),
        'page': Page.objects.first(),
        'cart_quantity': cart_quantity,
    }