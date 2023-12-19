from django.urls import path
from .views import *



urlpatterns = [
    path('getCategories/', categoriesViews.as_view(), name="getCategories"),
    path('getProducts/', productViews.as_view(), name="getProducts"),
    path('addToCart/', addToCartView.as_view(), name="addToCart"),
    path('checkOut/', CheckOutView.as_view(), name="checkOut"),
    path('productReviews/', ProductReview.as_view(), name="productReviews"),
]
   