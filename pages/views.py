from django.shortcuts import render, get_object_or_404, redirect
from .models import Treatment, ServiceCategory, Product, TeamMember, CartItem, Page, BlogPost

def dynamic_page_view(request, slug):
    page = get_object_or_404(Page, slug=slug)
    image_dict = {img.name: img.image.url for img in page.images.all()}
    return render(request, f"pages/{slug}.html", {'page': page, 'image_dict': image_dict})

def home_page_view(request):
    products = Product.objects.all()[:4]
    return render(request, 'pages/home.html', {'products': products})

def index_page_view(request):
    return render(request, "pages/index.html")

def error_page_view(request):
    return render(request, "pages/error.html")

def services_list_view(request):
    categories = ServiceCategory.objects.all()
    treatments = Treatment.objects.all()
    active_category_slug = request.GET.get('category')
    active_category = None
    if active_category_slug:
        treatments = treatments.filter(category__slug=active_category_slug)
        active_category = ServiceCategory.objects.filter(slug=active_category_slug).first()
    return render(request, 'pages/services.html', {
        'categories': categories,
        'treatments': treatments,
        'active_category': active_category,
    })

def service_detail_view(request, code):
    treatment = get_object_or_404(Treatment, treatment_code=code)
    related_services = Treatment.objects.filter(category=treatment.category).exclude(id=treatment.id)[:3]
    return render(request, 'pages/services_details.html', {
        'treatment': treatment,
        'related_services': related_services,
    })

def shop_overview_view(request):
    category_slug = request.GET.get('category')
    products = Product.objects.all().order_by('-id')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    return render(request, 'pages/shop.html', {'products': products})

def shop_detail_view(request, product_code):
    product = get_object_or_404(Product, product_code=product_code)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]
    return render(request, 'pages/shop_details.html', {
        'product': product, 
        'related_products': related_products
    })

def shop_category_view(request, slug):
    category = get_object_or_404(ServiceCategory, slug=slug)
    products = Product.objects.filter(category=category).order_by('-id')
    return render(request, 'pages/shop.html', {'products': products, 'category': category})

def add_to_cart(request, item_type, code):
    if item_type == 'product':
        item = get_object_or_404(Product, product_code=code)
        cart_item, created = CartItem.objects.get_or_create(
            product=item, 
            user=request.user if request.user.is_authenticated else None
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    return redirect('cart_page')

def cart_page_view(request):
    cart_items = CartItem.objects.filter(user=request.user, product__isnull=False)
    subtotal = sum(item.get_total_price() for item in cart_items)
    return render(request, "pages/cart.html", {
        'cart_items': cart_items, 
        'subtotal': subtotal
    })

def team_page_view(request):
    members = TeamMember.objects.all()
    return render(request, "pages/team.html", {'members': members})

def team_details_view(request, member_code):
    """
    Renders team details by fetching the member and 
    passing parsed skill/award/elective lists to the template.
    """
    member = get_object_or_404(TeamMember, member_code=member_code)
    
    return render(request, "pages/team_details.html", {
        'member': member,
        'skills': member.get_skills_list(),
        'awards': member.get_awards_list(),
        'electives': member.get_electives_list(),
    })

def checkout_page_view(request):
    return render(request, "pages/checkout.html")

def blog_grid_view(request):
    posts = BlogPost.objects.all().order_by('-date')
    return render(request, "pages/blog_grid.html", {'posts': posts})

def blog_details_view(request, slug):
    p = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'pages/blog_details.html', {
        'title': p.title,
        'author_name': p.author_name,
        'author_image': p.author_image.url if p.author_image else None,
        'category': p.category,
        'tags': p.tags,
        'date': p.date.strftime("%B %d, %Y"),
        'image_url': p.image.url,
        'video_url': p.video_url,
        'content': p.content,
        'image_1': p.post_image_1.url if p.post_image_1 else None,
        'image_2': p.post_image_2.url if p.post_image_2 else None,
    })