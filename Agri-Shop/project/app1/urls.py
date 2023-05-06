from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('about', about, name='about'),
    path('products/(?P<user>.)/$', products, name='products'),
    path('orders/(?P<user>.)/$', orders, name='orders'),
    path('create_order/(?P<user>.)/$', create_order, name='create_order'),
    path('dashboard/(?P<user>.)/$', dashboard, name='dashboard'),
    path('add_product/(?P<user>.)/$', add_product, name='add_product'),
    path('cart/(?P<user>.)/$', cart, name='cart'),
    path('edit_product/(?P<product_id>.)/$', edit_product, name='edit_product'),
    path('delete_product/(?P<product_id>.)/$', delete_product, name='delete_product'),
    path('logout', logout, name='logout'),
    path('', home, name='home'),

]
