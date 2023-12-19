from django.contrib import admin
from django.contrib.admin import register

from backend.models import *

@register(ParentCategory)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'created_at']
    
@register(Category)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'parent_category', 'created_at']
    
@register(Reviews)
class UserAdmin(admin.ModelAdmin):
    list_display = [ 'product', 'rating', 'created_at']
    
@register(Discount)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage', 'start_date', 'end_date']
    
@register(Brand)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    
@register(Product)
class UserAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'price', 'brand', 'inventory', 'category', 'id', 'slug']
    
# @register(ProductVariation)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['product', 'name', 'price', 'created_at']
    
@register(CartItmes)
class UserAdmin(admin.ModelAdmin):
    list_display = ['product', 'id', 'quantity', 'created_at']
    
@register(OrderItems)
class UserAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'id', 'created_at']
    
@register(Order)
class UserAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'status', 'created_at']

@register(UserItem)
class UserAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'is_in_cart' , 'created_at']

@register(Variation)
class UserADmin(admin.ModelAdmin):
    list_display = ['product' ,'variation_value' ,'is_active','created_date']
    
@register(VeriationsCategory)
class UserADmin(admin.ModelAdmin):
    list_display = ['name']