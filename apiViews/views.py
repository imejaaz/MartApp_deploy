from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import views 
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from backend.models import *

from .serializers import *

class categoriesViews(views.APIView):
    
    def get(self, request):

        pCategories = ParentCategory.objects.all()
        serializer = categorySerializer(pCategories, many = True)
        return Response(serializer.data, status=200)

  

    def post(self, request, *args, **kwargs):

        id = self.request.data.get('id')
        ctg_id = self.request.data.get('ctg_id')
        if id is not None:
            pc=ParentCategory.objects.get(id=id)
            subCategories=pc.subCat.all()
            serializer = subCatSerializer(subCategories, many = True)
            return Response({'status':200, 'message':'These are producs sub categories according to parent category', 'payload': serializer.data})
        
        if ctg_id is not None:
            ctg=Category.objects.get(id=ctg_id)
            products = ctg.products.all()
            serializer = productSerializer(products, many = True)
            return Response({'status':200, 'message':'These are products according to the category', 'payload': serializer.data})
        
        else:
            return Response({'message': 'input valid id please'})
        
class productViews(views.APIView):
    
    def get(self, request, *args, **kwargs):
        topSell = self.request.query_params.get('topSell')
        recommended = self.request.query_params.get('recommended')
        featured = self.request.query_params.get('featured')
        
        products = Product.objects.all()[:10]
        if topSell:
            products = Product.objects.filter(top_selling = True)
            
        if recommended:
            products = Product.objects.filter(is_recommended = True)
    
        if featured:
            products = Product.objects.filter(is_featured = True)
        
        serializer = productSerializer(products, many = True)
        return Response({ 'status': 200, 'message': 'These are products', 'payload': serializer.data })
        
    
    def post(self, request, *args, **kwargs):

        id = self.request.data.get('id')
        try:
            obj = Product.objects.get(id = id)
        except Exception as e:
            print("Error to get product by id", e) 
        serializer = productSerializer(obj)
        return Response({ 'status': 200, 'message': 'These are products', 'payload': serializer.data })
    
class addToCartView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        UserCartItems = CartItmes.objects.filter(user = user)
        if UserCartItems is not None:
            serializer = cartItemsSerializer(UserCartItems, many=True)
            return Response(serializer.data)
        else:
            return Response({"Message":"No Item in Cart"})
    
    def post(self, request, *args, **kwargs):
        
        id = request.data.get('id')
        quantity = request.data.get('quantity')
        
        if not id or not quantity: 
            raise ValidationError("Both Product ID and quantity are required.")

        try:
            productObj = Product.objects.get(id = id)
            
            User = get_user_model()
            user = User.objects.get(pk=request.user.pk)
            
            cartItemObj, created = CartItmes.objects.get(
                user = user,
                product = productObj,
                quantity = quantity
            )
            serializer = cartItemsSerializer(cartItemObj)
            return Response({ 'status': 201, 'message': 'Product add to cart successfully', 'payload': serializer.data })
        except Product.DoesNotExist:
            raise ValidationError("Product does not exist!")
    
    
    def delete(self, request, *args, **kwargs):
        id = request.data.get('id')

        if not id:
            raise ValidationError("Product ID is required to remove from cart.")

        try:
            product = Product.objects.get(id=id)

            User = get_user_model()
            user = User.objects.get(pk=request.user.pk)

            cart_item = CartItmes.objects.filter(user=user, product=product)
            if cart_item.exists():
                cart_item.delete()
                return Response(
                    {'status': 200, 'message': 'Product removed from cart successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                raise NotFound("Product not found in the cart.")

        except Product.DoesNotExist:
            raise ValidationError("Product does not exist!")
        

class CheckOutView(views.APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        orderObj = Order.objects.filter(user = user)
        serializer = orderSerializer(orderObj, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        cartItems = request.data.get('cartItems')
        phone = request.data.get('phone')
        recipient_name = request.data.get('recipient_name')
        address = request.data.get('address')
        city = request.data.get('city')
        total_price = request.data.get('total_price')
        
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        
        if cartItems is not None:
            orderObj = Order.objects.create(
                user = user,
                phone = phone,
                recipient_name = recipient_name,
                address = address,
                city = city,
                total_price = total_price,
            )
            for itemId in cartItems:
                cartObj = CartItmes.objects.get(id = itemId)
                orderItemObj = OrderItems.objects.create(
                    order = orderObj,
                    product = cartObj.product,
                    quantity = cartObj.quantity,
                    price = 3.22,
                )
                cartObj.delete()
            serializer = orderSerializer(orderObj)
            return Response({'status':200, "message":"Order placed successfully!", "payload":serializer.data })

class ProductReview(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        id = request.query_params.get('id')
        productObj = Product.objects.get(id = id)
        prodReviews = productObj.reviews.all()
        serializer = productReviewsSerializer(prodReviews, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        productId = request.data.get('productId')
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        
        prodObj = get_object_or_404(Product, id = productId)
        existingReview = Reviews.objects.filter(user = user, product = prodObj).exists()
       
    
        if existingReview:
            return Response({"Message":"You can only post one review per product!"}, status = status.HTTP_400_BAD_REQUEST)
        
        orderObj = get_object_or_404(Order, user = user) 
        
        if orderObj and (orderObj.status == 'completed'):
            print("condition passed")
            prodReviewObj = Reviews.objects.create(
                    user = user,
                    product = prodObj,
                    rating = rating, 
                    comment = comment
                )
            serializer = productReviewsSerializer(prodReviewObj)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response("You must have a completed order to post a review!", status=status.HTTP_400_BAD_REQUEST)
        