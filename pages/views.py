from django.shortcuts import render, get_object_or_404, redirect
from .models import Treatment, ServiceCategory, Product, TeamMember, CartItem, Page, PartnerLogo, BeautyGallery 
from .models import BlogPost, Comment, SiteImage, IndexPageContent,ServiceCategory, Testimonial, FAQ, GalleryImage, HomePageContent,UserProfile
from django.db.models import Count
from django.conf import settings
from .forms import (
    UserRegistrationForm, 
    CustomAuthenticationForm,
    UserProfileRegistrationForm, 
    UserUpdateForm, 
    ProfileUpdateForm,
    CommentForm,
    TeamInquiryForm
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import stripe
import os
import urllib.parse
stripe.api_key = settings.STRIPE_SECRET_KEY




#View for the main index page
def index_page_view(request):
    content = IndexPageContent.objects.first()
    main_about_text = content.about_description if content else ""

    img1 = f'<img src="{content.about_sm_img_01.url}" class="inline-img">'
    img2 = f'<img src="{content.about_sm_img_02.url}" class="inline-img">'
    img3 = f'<img src="{content.about_sm_img_03.url}" class="inline-img">'
    about_text = content.about_description
    about_text = about_text.replace("[IMG1]", img1)
    about_text = about_text.replace("[IMG2]", img2)
    about_text = about_text.replace("[IMG3]", img3)
 
    featured_categories = ServiceCategory.objects.all()[:3]
    beauty_images = BeautyGallery.objects.all().order_by('order')
    treatments = Treatment.objects.all()[:5]
    products = Product.objects.all()[:3]
    faq_data = FAQ.objects.first()
    gallery = GalleryImage.objects.all().order_by('order')
    posts = BlogPost.objects.all()[:3]
    partnerLogo = PartnerLogo.objects.filter(template_type='index_page')[:10]
   
    return render(request, 'pages/index.html', {
        'content': content,
        'featured_list': featured_categories,
        'about_description_html': about_text,
        'beauty_images':beauty_images,
        'treatment_list': treatments,
        'product_list': products,
        'main_about_text': main_about_text,
        'faq_list': faq_data,
        'gallery_list': gallery,
        'posts': posts,
        'partnerLogo': partnerLogo
        
    })





#User registration View
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        profile_form = UserProfileRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
        profile_form = UserProfileRegistrationForm()
        
    return render(request, 'pages/register.html', {
        'form': form,
        'profile_form': profile_form
    })


#User update profile View
@login_required
def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('index')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
        
    return render(request, 'pages/profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })


#User login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'pages/login.html', {'form': form})





#View for the services list page
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


#view for the service details page
def service_detail_view(request, code):
    treatment = get_object_or_404(Treatment, treatment_code=code)
    related_services = Treatment.objects.filter(category=treatment.category).exclude(id=treatment.id)[:3]
    benefits_list = []
    if treatment.grid_benefits_data:
        items = treatment.grid_benefits_data.split('\n')
        for item in items:
            parts = item.split('|')
            if len(parts) >= 2:
                benefits_list.append({
                    'title': parts[0].strip(),
                    'description': parts[1].strip(),
                })
    bullet_list = []
    if treatment.bullet_benefits:
        bullet_list = [line.strip() for line in treatment.bullet_benefits.split('\n') if line.strip()]
    return render(request, 'pages/services_details.html', {
        'treatment': treatment,
        'related_services': related_services,
        'benefits_list': benefits_list,
        'bullet_list': bullet_list,
    })





#Function to display all products or selected category products
def shop_view(request, slug=None):
    category = None
    products = Product.objects.all().order_by('-id')
    
    if slug:
        category = get_object_or_404(ServiceCategory, slug=slug)
        products = products.filter(category=category)
        
    return render(request, 'pages/shop.html', {
        'products': products,
        'category': category  
    })


#Fuction to handle single selected product page
def shop_detail_view(request, product_code):
    product = get_object_or_404(Product, product_code=product_code)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]
    similar_products = Product.objects.filter(name=product.name)
    bullet_list = []
    if product.bullet_benefits:
        bullet_list = [line.strip() for line in product.bullet_benefits.split('\n') if line.strip()]
    
    if request.method == 'POST':
        return add_to_cart(request, 'product', product.product_code)

    return render(request, 'pages/shop_details.html', {
        'product': product, 
        'related_products': related_products,
        'bullet_list': bullet_list,
        'similar_products': similar_products
    })


#Function to handle selected product into cart  
def add_to_cart(request, item_type, code):
    if not request.user.is_authenticated:
        return redirect('login')

    if item_type == 'product':
        item = get_object_or_404(Product, product_code=code)
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(
            product=item, 
            user=request.user
        )
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
    return redirect('cart_page')


#Function to view the entrire cart   
def cart_page_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.get_total_price() for item in cart_items)
    return render(request, "pages/cart.html", {
        'cart_items': cart_items, 
        'subtotal': subtotal
    })


#Function to checkout the products and process the payment using stripe
def checkout_page_view(request):
    if not request.user.is_authenticated:
        return redirect('login') 

    # Ensure Stripe API key is set
    stripe.api_key = settings.STRIPE_SECRET_KEY

    cart_items = CartItem.objects.filter(user=request.user)
    
    # Redirect if the cart is empty
    if not cart_items.exists():
        return redirect('cart_page')

    cart_total = sum(item.get_total_price() for item in cart_items)
    amount_in_cents = int(cart_total * 100)
    error_message = None

    if request.method == 'POST':
        payment_intent_id = request.POST.get('payment_intent_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if payment_intent_id:
            try:
                intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                if intent.status == 'succeeded':
                    # TODO: If you want to save an Order model using first_name, last_name, etc., do it here!
                    
                    # Clear the user's cart items
                    cart_items.delete()
                    return redirect('order_success')
            except Exception as e:
                print(f"Stripe Error: {e}")
                
        error_message = 'Payment failed or was declined. Please try again.'        

    client_secret = None
    if amount_in_cents > 0:
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency='aed',
                payment_method_types=['card'],
            )
            client_secret = intent.client_secret
        except stripe.error.StripeError as e:
            error_message = str(e)
       
    return render(request, 'pages/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'amount_in_cents': amount_in_cents,
        'error_message': error_message,
        'STRIPE_PUBLISHABLE_KEY': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', None),
        'client_secret': client_secret,
    })

#Function to handle the order success page after successful payment
def order_success_view(request):
    return render(request, "pages/error.html")






def get_initial_user_data(request):
    initial_data = {}
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': getattr(profile, 'phone_number', ''),  # Adjust to your UserProfile phone field name if different
        }
    return initial_data

def dynamic_page_view(request, slug):
    page = get_object_or_404(Page, slug=slug)
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    partnerLogo = PartnerLogo.objects.filter(template_type='aboutus_page')[:10]
    image_dict = {img.name: img.image.url for img in page.images.all()}
    faq_obj = FAQ.objects.first()
    faq_list = []
    
    if faq_obj:
        for i in range(1, 5):
            question = getattr(faq_obj, f'q{i}', '')
            answer = getattr(faq_obj, f'a{i}', '')
            if question:
                faq_list.append({'question': question.strip(), 'answer': answer.strip()})
                
    context = {
        'page': page, 
        'image_dict': image_dict,
        'faqs': faq_list,
        'faq_obj' : faq_obj,
        'team_members': team_members,
        'testimonials': testimonials,
        'partnerLogo': partnerLogo,
    }
    
    if slug == 'contact':
        if request.method == 'POST':
            form = TeamInquiryForm(request.POST)
            if form.is_valid():
                inquiry = form.save(commit=False)
                
                # Assign to team member with role 'manager', or fallback to the first member
                target_member = TeamMember.objects.filter(role__icontains='manager').first()
                if not target_member:
                    target_member = TeamMember.objects.first()
                
                if target_member:
                    inquiry.team_member = target_member
                
                inquiry.save()
                
                # Extract form details including new fields
                first_name = form.cleaned_data.get('first_name', '')
                last_name = form.cleaned_data.get('last_name', '')
                email = form.cleaned_data.get('email', '')
                phone = form.cleaned_data.get('phone', '')
                subject = form.cleaned_data.get('subject', 'General Contact Inquiry')
                user_message = form.cleaned_data.get('message', '')
                
                # Format WhatsApp message text
                member_name = target_member.name if target_member else "Team"
                wa_text = (
                    f"Hello {member_name},\n\n"
                    f"You have a new website inquiry:\n"
                    f"*Name:* {first_name} {last_name}\n"
                    f"*Email:* {email}\n"
                    f"*Mobile:* {phone}\n"
                    f"*Subject:* {subject}\n"
                    f"*Message:* {user_message}"
                )
                encoded_text = urllib.parse.quote(wa_text)
                
                # Route to manager's phone or fallback to page phone
                target_phone = target_member.phone if (target_member and target_member.phone) else (page.phone_field.split(',')[0] if page.phone_field else "1234567890")
                phone_number = "".join(filter(str.isdigit, target_phone))
                whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_text}"
                
                return redirect(whatsapp_url)
        else:
            # Pre-populate form fields if user is authenticated
            form = TeamInquiryForm(initial=get_initial_user_data(request))
            
        context.update({
            'form': form,
            'email_list': [e.strip() for e in page.email_field.split(',')] if page.email_field else [],
            'phone_list': [p.strip() for p in page.phone_field.split(',')] if page.phone_field else []
        })
        return render(request, 'pages/contact.html', context)
    else:
        return render(request, f"pages/{slug}.html", context)




#Function to handle the team details page and display the selected team member's details
def team_details_view(request, member_code):
    member = get_object_or_404(TeamMember, member_code=member_code)
    awards = [tuple(a.split('|')) for a in member.awards.split(';') if a] if member.awards else []
    skills = []
    electives = [e.strip() for e in member.electives.split(',')] if member.electives else []
    
    if request.method == 'POST':
        form = TeamInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.team_member = member
            inquiry.save()
            
            first_name = form.cleaned_data.get('first_name', '')
            last_name = form.cleaned_data.get('last_name', '')
            email = form.cleaned_data.get('email', '')
            phone = form.cleaned_data.get('phone', '')
            subject = form.cleaned_data.get('subject', 'Team Booking')
            user_message = form.cleaned_data.get('message', '')
            
            wa_text = (
                f"Hello {member.name},\n\n"
                f"You have a new booking/inquiry from your page:\n"
                f"*Name:* {first_name} {last_name}\n"
                f"*Email:* {email}\n"
                f"*Mobile:* {phone}\n"
                f"*Subject:* {subject}\n"
                f"*Message:* {user_message}"
            )
            encoded_text = urllib.parse.quote(wa_text)
            
            target_phone = member.phone if member.phone else "1234567890"
            phone_number = "".join(filter(str.isdigit, target_phone))
            whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_text}"
            
            return redirect(whatsapp_url)
    else:
        form = TeamInquiryForm(initial=get_initial_user_data(request))
        
    context = {
        'member': member,
        'awards': awards,
        'skills': skills,
        'electives': electives,
        'form': form,
    }
    return render(request, 'pages/team_details.html', context)





#Function to handle the blog grid page and display all the blog posts
def blog_grid_view(request):
    posts = BlogPost.objects.all().order_by('-date')
    return render(request, "pages/blog_grid.html", {'posts': posts})


#Function to handle the blog details page and display the selected blog post along with comments and related posts
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





def error_page_view(request):
    return render(request, "pages/error.html")






def home_page_view(request):
    content = HomePageContent.objects.first()
    partner = PartnerLogo.objects.all()
    products = Product.objects.all()[:4]
    treatments = Treatment.objects.all()
    teammembers = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    return render(request, 'pages/home.html', {
        'content': content,
        'products': products,
        'partners':partner,
        'treatments':treatments,
        'teammembers':teammembers,
        'testimonials':testimonials
        })






