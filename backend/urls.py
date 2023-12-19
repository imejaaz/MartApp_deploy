from . import views 
from django.urls import path
urlpatterns = [
    path('', views.Categories, name='categories'),
    path('product_by_ctg/<id>', views.ProductByCtg, name='product_by_ctg'),
    path('product_details/<id>', views.ProductDetails, name='product_details'),
    
]