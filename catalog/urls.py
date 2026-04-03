from django.urls import path
from . import views

app_name = 'catalog'  

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.category_list, name='category_list'),
    path('product/<slug:slug>/', views.product_list, name='product_list_by_category'),
    path('product/detail/<slug:slug>/', views.product_detail, name='product_detail'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart_view, name='cart_view'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove'),
    path('my-orders/', views.my_orders, name='my_orders'),
]