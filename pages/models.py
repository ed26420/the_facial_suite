from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', default='profiles/default.png', blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    def __str__(self):
        return self.user.username
    
class IndexPageContent(models.Model):
    # Hero Section
    hero_title = models.CharField(max_length=200)
    hero_subtitle = models.TextField()
    hero_bg_image = models.ImageField(upload_to='index_images/')
    
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

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name 

class Treatment(models.Model):
    treatment_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='treatments')
    name = models.CharField(max_length=150)
    services_page_description = models.TextField(blank=True, null=True)
    subtitle_tags = models.CharField(max_length=200, default="Facial, Glow")
    main_thumbnail = models.ImageField(upload_to='services/cards/')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    hero_banner_image = models.ImageField(upload_to='services/banners/')
    details_about_paragraph_1 = models.TextField(blank=True, null=True)
    details_about_paragraph_2 = models.TextField(blank=True, null=True)
    mid_page_image = models.ImageField(upload_to='services/details/')
    usage_instructions = models.TextField(blank=True, null=True)
    grid_benefits_data = models.TextField(blank=True, null=True)
    benefits_intro_text = models.TextField(blank=True, null=True)
    bullet_benefits = models.TextField(blank=True, null=True)
    details_second_image_bg = models.ImageField(upload_to='services/details_bg/', blank=True, null=True)

    def __str__(self):
        return f"{self.treatment_code or 'NO CODE'} - {self.name}"

class Product(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='products')
    product_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    short_description = models.CharField(max_length=255)
    full_description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    sizes = models.CharField(max_length=150, default="100ml, 200ml")
    additional_info_text = models.TextField(blank=True, null=True)
    bullet_benefits = models.TextField(blank=True, null=True)
    main_image = models.ImageField(upload_to='shop/products/')
    gallery_image_2 = models.ImageField(upload_to='shop/gallery/', blank=True, null=True)
    gallery_image_3 = models.ImageField(upload_to='shop/gallery/', blank=True, null=True)
    gallery_image_4 = models.ImageField(upload_to='shop/gallery/', blank=True, null=True)
    gallery_image_5 = models.ImageField(upload_to='shop/gallery/', blank=True, null=True)

    def __str__(self):
        return f"{self.product_code} - {self.name}"

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

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)

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

class Page(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    story_text = models.TextField(blank=True, null=True) # Included
    email_field = models.TextField(blank=True, null=True, help_text="Enter emails separated by commas")
    phone_field = models.TextField(blank=True, null=True, help_text="Enter phone numbers separated by commas")
    address = models.TextField(blank=True, null=True)
    faq_data = models.TextField(blank=True, null=True, help_text="Format: Question|Answer, Question|Answer") # Included

    def __str__(self):
        return self.title

class SiteImage(models.Model):
    page = models.ForeignKey(Page, related_name='images', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='site_assets/')