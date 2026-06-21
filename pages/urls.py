from django.urls import path
from .views import (
    home_page_view, 
    services_list_view, 
    cart_page_view, 
    checkout_page_view, 
    index_page_view, 
    service_detail_view, 
    shop_overview_view, 
    shop_detail_view, 
    shop_category_view, 
    add_to_cart, 
    dynamic_page_view,
    team_page_view,
    team_details_view,
    blog_grid_view,
    blog_details_view
)

urlpatterns = [
    path('', home_page_view, name='home'),
    path('index/', index_page_view, name='index'),

    path('services/', services_list_view, name='services'),
    path('services/<str:code>/', service_detail_view, name='services_details'),

    path('shop/', shop_overview_view, name='shop'),
    path('shop/<str:product_code>/', shop_detail_view, name='shop_details'),
    path('shop/category/<slug:slug>/', shop_category_view, name='shop_category'),

    path('cart/', cart_page_view, name='cart_page'),
    path('add-to-cart/<str:item_type>/<str:code>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout_page_view, name='checkout'),

    path('team/', team_page_view, name='team'),
    path('team/<slug:member_code>/', team_details_view, name='team_details'),
    
    path('blog-grid/', blog_grid_view, name='blog_grid'),
    path('blog/<slug:slug>/', blog_details_view, name='blog_detail'),

    path('about/', dynamic_page_view, {'slug': 'about'}, name='about'),
    path('team/', dynamic_page_view, {'slug': 'team'}, name='team'),
    path('team-details/', dynamic_page_view, {'slug': 'team_details'}, name='team_details'),
    path('contact/', dynamic_page_view, {'slug': 'contact'}, name='contact'),
    
    
    path('error-page/', dynamic_page_view, {'slug': 'error'}, name='error_page'),
]