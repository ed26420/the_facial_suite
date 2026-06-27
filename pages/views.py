from django.shortcuts import render, get_object_or_404, redirect
from .models import Treatment, ServiceCategory, Product, TeamMember, CartItem, Page 
from .models import BlogPost, Comment, SiteImage, IndexPageContent,ServiceCategory
from django.db.models import Count
from .forms import CommentForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

def dynamic_page_view(request, slug):
    page = get_object_or_404(Page, slug=slug)
    image_dict = {img.name: img.image.url for img in page.images.all()}
    about_page = Page.objects.filter(slug='about').first()
    faq_list = []
    if about_page and about_page.faq_data:
        for item in about_page.faq_data.split(','):
            parts = item.split('|')
            if len(parts) == 2:
                faq_list.append({'question': parts[0].strip(), 'answer': parts[1].strip()})
    if slug == 'contact':
        return render(request, 'pages/contact.html', {
            'page': page, 
            'image_dict': image_dict,
            'faqs': faq_list,
            'email_list': [e.strip() for e in page.email_field.split(',')] if page.email_field else [],
            'phone_list': [p.strip() for p in page.phone_field.split(',')] if page.phone_field else []
        })
    else:
        return render(request, f"pages/{slug}.html", {
            'page': page, 
            'image_dict': image_dict,
            'faqs': faq_list
        })

def home_page_view(request):
    products = Product.objects.all()[:4]
    return render(request, 'pages/home.html', {'products': products})

def index_page_view(request):
    content = IndexPageContent.objects.first()

    img1 = f'<img src="{content.about_sm_img_01.url}" class="inline-img">'
    img2 = f'<img src="{content.about_sm_img_02.url}" class="inline-img">'
    img3 = f'<img src="{content.about_sm_img_03.url}" class="inline-img">'
    
    about_text = content.about_description
    about_text = about_text.replace("[IMG1]", img1)
    about_text = about_text.replace("[IMG2]", img2)
    about_text = about_text.replace("[IMG3]", img3)

    faq_list = []
    main_about_text = content.about_description if content else ""
    if content and "FAQ_START" in content.about_description:
        main_about_text, faq_raw = content.about_description.split("FAQ_START")
        for item in faq_raw.split(','):
            parts = item.split('|')
            if len(parts) == 2:
                faq_list.append({
                    'question': parts[0].strip(), 
                    'answer': parts[1].strip()
                })
    featured_categories = ServiceCategory.objects.all()[:3]
    treatments = Treatment.objects.all()[:4]
    products = Product.objects.all()[:3]
    posts = BlogPost.objects.all()[:3]
    blog_list = [
        {
            'title': post.title,
            'image_url': post.image.url if post.image else None,
            'date': post.date.strftime("%B %d, %Y"),
            'author': post.author_name,
            'url': post.get_absolute_url()
        }
        for post in posts
    ]
    return render(request, 'pages/index.html', {
        'content': content,
        'main_about_text': main_about_text,
        'faq_list': faq_list,
        'treatment_list': treatments,
        'product_list': products,
        'blog_list': blog_list,
        'featured_list': featured_categories,
        'about_description_html': about_text,
    })



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
    latest_posts = BlogPost.objects.exclude(slug=slug).order_by('-date')[:4]
    categories = BlogPost.objects.values('category').annotate(count=Count('category'))
    comments = p.comments.filter(active=True)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.blog_post = p
            new_comment.user = request.user
            new_comment.save()
            return redirect('blog_detail', slug=p.slug)
    else:
        form = CommentForm()

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
        'latest_posts': latest_posts,
        'categories': categories,
        'comments': comments,
        'comment_form': form,
    })

@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'pages/profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'pages/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})