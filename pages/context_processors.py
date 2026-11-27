from django.db.models import Sum
from .models import ServiceCategory, BasePageContent, Page, CartItem, TeamMember


def menu_categories(request):
    cart_quantity = 0
    if request.user.is_authenticated:
        result = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))
        cart_quantity = result['total'] or 0

    categories = ServiceCategory.objects.prefetch_related('treatments').all()

    receptionist = TeamMember.objects.filter(role__icontains="receptionist").first()
    receptionist_whatsapp = ""
    if receptionist and receptionist.phone:
        receptionist_whatsapp = "".join(filter(str.isdigit, receptionist.phone))

    return {
        'menu_categories': categories,
        'base': BasePageContent.objects.first(),
        'page': Page.objects.first(),
        'cart_quantity': cart_quantity,
        'receptionist_whatsapp': receptionist_whatsapp,
    }