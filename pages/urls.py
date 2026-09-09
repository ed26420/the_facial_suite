from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from .views import (
    home_page_view, 
    profile_edit,
    services_list_view, 
    cart_page_view, 
    checkout_page_view, 
    index_page_view, 
    service_detail_view, 
    shop_view, 
    shop_detail_view, 
    add_to_cart, 
    dynamic_page_view,
    team_details_view,
    blog_grid_view,
    blog_details_view,
    register_view,
    login_view,
    order_success_view
)

urlpatterns = [
    path('', index_page_view, name='index'),
    path('index/', home_page_view, name='home'),

    path('register/', register_view, name='register'),
    path('profile/', profile_edit, name='profile'),
    path('login/', login_view, name='login'),

    path('services/', services_list_view, name='services'),
    path('services/<str:code>/', service_detail_view, name='services_details'),

    path('shop/', shop_view, name='shop'),
    path('shop/category/<slug:slug>/', shop_view, name='shop_category'),
    path('shop/<str:product_code>/', shop_detail_view, name='shop_details'),
    path('add-to-cart/<str:item_type>/<str:code>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_page_view, name='cart_page'),
    path('checkout/', checkout_page_view, name='checkout'),
    path('checkout/success/', order_success_view, name='order_success'),

    path('about/', dynamic_page_view, {'slug': 'about'}, name='about'),
    path('contact/', dynamic_page_view,{'slug': 'contact'}, name='contact'),
    path('team/<slug:member_code>/', team_details_view, name='team_details'),


    path('blog-grid/', blog_grid_view, name='blog_grid'),
    path('blog/<slug:slug>/', blog_details_view, name='blog_detail'),    

    path('error-page/', dynamic_page_view, {'slug': 'error'}, name='error_page'),

    path('home/', home_page_view, name='home'),

    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='pages/password_reset.html',
            form_class=CustomPasswordResetForm
            ), 
         name='password_reset'),

         
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='pages/password_reset_done.html'), 
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='pages/password_reset_confirm.html',
             form_class=CustomSetPasswordForm
         ), 
         name='password_reset_confirm'),

    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='pages/password_reset_complete.html'), 
         name='password_reset_complete'),
]

