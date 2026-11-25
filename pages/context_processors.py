from .models import ServiceCategory, BasePageContent, Page, CartItem
from django.db.models import Sum
from .models import TeamMember

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

def site_context(request):  # Add this inside your existing context processor
    receptionist = TeamMember.objects.filter(role__icontains="receptionist").first()
    receptionist_whatsapp = ""
    if receptionist and receptionist.phone:
        receptionist_whatsapp = "".join(filter(str.isdigit, receptionist.phone))

    return {
        # ... your existing context keys ...
        "receptionist_whatsapp": receptionist_whatsapp,
    }