from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .models import (
    ServiceCategory, Treatment, Product, CartItem, 
    TeamMember, BlogPost, Page, SiteImage, Comment, IndexPageContent
)


class SiteImageInline(admin.TabularInline):
    model = SiteImage
    extra = 1


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug')

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name', 'treatment_code', 'price')
    search_fields = ('name', 'treatment_code')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('product_code', 'name', 'category', 'price', 'rating')
    list_filter = ('category',)
    search_fields = ('name', 'product_code')
    fieldsets = (
        ('Basic Information', {
            'fields': ('product_code', 'name', 'category', 'short_description', 'full_description')
        }),
        ('Additional Details', { 
            'fields': ('additional_info_text', 'bullet_benefits'),
        }),
        ('Pricing & Ratings', {
            'fields': ('price', 'discount_price', 'rating', 'sizes')
        }),
        ('Product Images Gallery', {
            'fields': ('main_image', 'gallery_image_2', 'gallery_image_3', 'gallery_image_4', 'gallery_image_5')
        }),
    )

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('product', 'quantity', 'user', 'session_id')
    list_filter = ('user',)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name', 'role')

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [SiteImageInline]
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'story_text')}),
        ('Contact Info (For Contact Page)', {
            'fields': ('email_field', 'phone_field', 'address'),
            'classes': ('collapse',),
        }),
        ('FAQ Data (About & Contact Pages)', {
            'fields': ('faq_data',),
            'description': "Format: Question|Answer,Question|Answer. Use | to separate question from answer, and , to separate items.",
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 40})},
    }
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name', 'page')
    list_filter = ('page',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    save_as = True
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'date', 'author_name')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'author_name', 'author_image')
        }),
        ('Media & Gallery', {
            'fields': ('image', 'video_url', 'post_image_1', 'post_image_2')
        }),
        ('Content', {
            'fields': ('summary', 'content', 'tags')
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('user', 'body', 'blog_post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']
    
    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        queryset.update(active=True)

@admin.register(IndexPageContent)
class IndexPageAdmin(admin.ModelAdmin):
    list_display = ('__str__',)