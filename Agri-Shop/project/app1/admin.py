from django.contrib import admin
from .models import Farmer, Client, Product, Order, OrderItem


class FarmerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'dob', 'nationality')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_price', 'quantity_in_stock', 'category', 'farmer','image')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'date_ordered', 'payment_type')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')


admin.site.register(Farmer, FarmerAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
