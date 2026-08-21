from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse





#Model for main index page  
class IndexPageContent(models.Model):
    # Hero Section
    hero_title = models.CharField(max_length=200)
    hero_subtitle = models.TextField()
    hero_bg_image = models.ImageField(upload_to='index_images/')

    # Suite Section
    suite_description = models.TextField(max_length=255, blank=True, null=True)
    
    # About Section (FAQ logic will be extracted from the description)
    about_subtitle = models.CharField(max_length=100, default="About Us")
    about_description = models.TextField(help_text="Include FAQ items here using format: Question|Answer,Question|Answer")
    about_sm_img_01 = models.ImageField(upload_to='index_images/')
    about_sm_img_02 = models.ImageField(upload_to='index_images/')
    about_sm_img_03 = models.ImageField(upload_to='index_images/')
    
    # Stats
    about_box_01_stat = models.CharField(max_length=10) 
    about_box_01_text = models.CharField(max_length=100) 
    about_box_02_stat = models.CharField(max_length=10)
    about_box_02_text = models.CharField(max_length=100)

    stats_img_01 = models.ImageField(upload_to='stats/', blank=True, null=True)
    stats_img_02 = models.ImageField(upload_to='stats/', blank=True, null=True)

    def __str__(self):
        return "Complete Index Page Configuration"


    def __str__(self):
        return "Index Page Content Configuration" 





#Model user profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', default='profiles/default.png', blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    residential_address = models.TextField(blank=True)
    def __str__(self):
        return self.user.username
    
   



#Model for Services categories   
class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name 


#Model for Treatments
class Treatment(models.Model):
    treatment_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='treatments')
    name = models.CharField(max_length=150)
    services_page_description = models.TextField(blank=True, null=True)
    subtitle_tags = models.CharField(max_length=200, default="Facial, Glow")
    main_thumbnail = models.ImageField(upload_to='services/cards/')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    hero_banner_image = models.ImageField(upload_to='services/banners/')
    mid_page_image = models.ImageField(upload_to='services/details/')
    usage_instructions = models.TextField(blank=True, null=True)
    grid_benefits_data = models.TextField(blank=True, null=True)
    benefits_intro_text = models.TextField(blank=True, null=True)
    bullet_benefits = models.TextField(blank=True, null=True)
    details_about_paragraph_1 = models.TextField(blank=True, null=True)
    details_about_paragraph_2 = models.TextField(blank=True, null=True)
    details_second_image_bg = models.ImageField(upload_to='services/details_bg/', blank=True, null=True)

    def __str__(self):
        return f"{self.treatment_code or 'NO CODE'} - {self.name}"





#Model for Products in the shop
class Product(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='products')
    product_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    short_description = models.CharField(max_length=255)
    full_description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    sizes = models.CharField(max_length=150, default="100ml")
    additional_info_text = models.TextField(blank=True, null=True)
    bullet_benefits = models.TextField(blank=True, null=True)
    main_image = models.ImageField(upload_to='shop/products/')
    gallery_image_2 = models.ImageField(upload_to='shop/gallery/', blank=True, null=True)
    gallery_image_3 = models.ImageField(upload_to='shop/gallery/', blank=True, null=True)
    gallery_image_4 = models.ImageField(upload_to='shop/gallery/', blank=True, null=True)
    gallery_image_5 = models.ImageField(upload_to='shop/gallery/', blank=True, null=True)

    def __str__(self):
        return f"{self.product_code} - {self.name}"
    
    @property
    def size_list(self):
        return [size.strip() for size in self.sizes.split(',')]


#Model for products added to the cart
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def get_total_price(self):
        return self.product.price * self.quantity


#Model for products extra images
class BeautyGallery(models.Model):
    main_image = models.ImageField(upload_to='gallery/')
    photoname = models.CharField(max_length=100, default="Gallery Image")
    photodescription = models.CharField(max_length=100, default="Gallery Image")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']




#Model for Team Members
class TeamMember(models.Model):
    member_code = models.SlugField(unique=True, max_length=50)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    experience = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='team/')
    awards = models.TextField(help_text="Format: Title|Year|Description||Title|Year|Description")
    skills = models.TextField(help_text="Format: Skill Name:Percentage|Skill Name:Percentage")
    electives = models.TextField(help_text="Enter electives separated by |")
    electives_description = models.TextField(default="Specialized electives focus on advanced topics.")

    def __str__(self):
        return self.name

    def get_awards_list(self):
        data = []
        if self.awards:
            for block in self.awards.split('||'):
                parts = block.split('|')
                if len(parts) >= 3:
                    data.append(parts)
        return data

    def get_skills_list(self):
        skills_data = []
        if self.skills:
            items = self.skills.split('|')
            for item in items:
                if ':' in item:
                    name, percent = item.split(':', 1)
                    skills_data.append({'name': name.strip(), 'percent': percent.strip()})
        return skills_data

    def get_electives_list(self):
        if self.electives:
            return [e.strip() for e in self.electives.split('|') if e.strip()]
        return []




#Model for Team Member Inquiries
class TeamInquiry(models.Model):
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='inquiries', blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.team_member.name if self.team_member else "General Contact Page"
        return f"Inquiry for {target} by {self.first_name}"




#Model for Blog Posts
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='blog/', help_text="Main thumbnail")
    video_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    author_name = models.CharField(max_length=100)
    author_image = models.ImageField(upload_to='blog/authors/', default='defaults/author.png')
    tags = models.CharField(max_length=100)
    summary = models.TextField() 
    content = RichTextField() 
    post_image_1 = models.ImageField(upload_to='blog/details/', blank=True, null=True)
    post_image_2 = models.ImageField(upload_to='blog/details/', blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


#Models for Comments on Blog Posts
class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    class Meta:
        ordering = ['created_on']
    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog_post.title}'


#Model for dynamic pages like About, Contact, etc.
class Page(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    story_text = models.TextField(blank=True, null=True) # Included
    story_text_two = models.TextField(blank=True, null=True) # Included
    email_field = models.TextField(blank=True, null=True, help_text="Enter emails separated by commas")
    phone_field = models.TextField(blank=True, null=True, help_text="Enter phone numbers separated by commas")
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


#Model for images associated with dynamic pages
class SiteImage(models.Model):
    page = models.ForeignKey(Page, related_name='images', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='site_assets/')





#Model for FAQ Section    
class FAQ(models.Model):
    title = models.CharField(max_length=100, default="Frequently Asked Questions")
    image = models.ImageField(upload_to='faq/')
    q1 = models.CharField(max_length=255)
    a1 = models.TextField()
    q2 = models.CharField(max_length=255)
    a2 = models.TextField()
    q3 = models.CharField(max_length=255)
    a3 = models.TextField()
    q4 = models.CharField(max_length=255)
    a4 = models.TextField()
    def __str__(self):
        return self.title




#Model for Gallery Images
class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    alt_text = models.CharField(max_length=100, default="Gallery Image")
    instagram_url = models.URLField(help_text="Link to Instagram post", blank=True, null=True)
    facebook_url = models.URLField(help_text="Link to Facebook post", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']




#model for Home Page Content
class HomePageContent(models.Model):
    
    banner_title = models.CharField(max_length=200, default="Let Your Skin Breathe")
    banner_description = models.TextField(default="Let your skin breathe naturally with our gentle, nourishing formulas designed to cleanse, hydrate, and restore")
    banner_text_img = models.ImageField(upload_to='home/banner/', help_text="The style image next to the title")

    banner_product_img = models.ImageField(upload_to='home/banner/', help_text="The product image in the bottom left")
    main_banner_thumb = models.ImageField(upload_to='home/banner/', help_text="The main center thumbnail image")
    video_bg_img = models.ImageField(upload_to='home/banner/', help_text="The video background image")
    
    video_url = models.URLField(help_text="Link to the promotional video")
    
    client_img = models.ImageField(upload_to='home/banner/', help_text="The client testimonial images")
    satisfied_clients_count = models.PositiveIntegerField(default=67, help_text="Number in thousands (e.g., 67 for 67k+)")

    about_description_main = models.TextField(default="let")
    about_description_two = models.TextField(default="let")
    about_image = models.ImageField(upload_to='home/about/')

    chooseus_image = models.ImageField(upload_to='home/about/')
    chooseus_text_one = models.TextField(default="Trained professionals delivering trusted skincare treatments.")
    chooseus_text_two = models.TextField(default="We never test on animals and use only ethically sourced safe ingredients")
    chooseus_text_three = models.TextField(default="Personalized treatments crafted to meet your unique skin type and concerns.")
    chooseus_text_four = models.TextField(default="Sustainable, cruelty-free practices that care for you and the planet.")
    chooseus_text_five = models.TextField(default="Loved by skincare enthusiasts worldwide, with thousands of happy glowing customers.")

    treatment_text_one = models.TextField(default="Discover personalized skincare treatments designed to meet your unique needs. From deep cleansing facials to targeted therapies, our expert care helps you achieve healthy, glowing, and beautiful.")
    def __str__(self):
        return "Home Page Content"





#model for Partner Logos
class PartnerLogo(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners/')
    order = models.PositiveIntegerField(default=0, help_text="Order in the slider")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name





#model for Testimonials
class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_position = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    review_text = models.TextField()
    small_image = models.ImageField(upload_to='testimonials/small/', help_text="Used in slider cards")
    background_image = models.ImageField(upload_to='testimonials/background/', blank=True, null=True)
    
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.client_name





#Model for Staff Reviews
class StaffReview(models.Model):
    staff_name = models.CharField(max_length=100)
    client_position = models.CharField(max_length=100)
    large_image = models.ImageField(upload_to='reviews/')
    review_text = models.TextField()
    match_rate = models.CharField(max_length=10, default="100%")

    def __str__(self):
        return self.staff_name


