import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, OTP 
from django.contrib.auth.hashers import make_password
from .utils import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, ValidationError
from .serializer import *
from rest_framework.permissions import IsAuthenticated








# import vonage

# def send_sms(request):

    # client = vonage.Client(key="a91b0762", secret="Bn2GGqPQCAeAyR0A")
    # sms = vonage.Sms(client)

    # responseData = sms.send_message(
        # {
    #         "from": "Vonage APIs",
    #         "to": "923088976204",
    #         "text": "A text message sent using the Nexmo SMS API",
    #     }
    # )

    # if responseData["messages"][0]["status"] == "0":
    #     print("Message sent successfully.")
    #     return HttpResponse('Message send successfully')
    # else:
    #     print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
    #     return HttpResponse('Message faield due to some errors.')

def alert(request):
    return render(request, 'alert.html')

def requestOtp(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        if phone and phone[0] == '0':
            messages.error(request, "Enter Phone Number Without 0")
            return HttpResponseRedirect(request.path_info)
        if len(phone)  is not 10:
            messages.error(request, "Invalid Phone Number!")
            return HttpResponseRedirect(request.path_info)
        if phone:
            if User.objects.filter(phone = phone).exists():
                messages.error(request, "Phone already exists!")
                return HttpResponseRedirect(request.path_info)
            
            response = send_otp(phone)
            messages.success(request, response)
            return redirect('verifyOtp', phone) 
        
        else:
            messages.error(request, "Phone number required!")
            return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/requestOtp.html')


def verifyOtp(request, phone):
    if request.method == "POST":
        otp = request.POST.get('otp')
        
        otp_obj = get_object_or_404(OTP, phone = phone, verified = False)
        
        if otp_obj.validity.replace(tzinfo=None) > datetime.datetime.utcnow():
            if otp_obj.otp == int(otp):
                otp_obj.verified = True 
                otp_obj.save()
                messages.success(request, 'OTP Verified Successfully!')
                return redirect('createAccount', phone)
                    
            messages.error(request, "Please Enter the currect OTP!")
            return HttpResponseRedirect(request.path_info)
                
        else:
            messages.info(request, "OTP Expired!")
            return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/verifyOtp.html', {"phone":phone})
    
    

def createAccount(request, phone):
    if request.method == "POST":
        image = request.FILES.get('image')

        max_size = 3 * 1024 * 1024  # 3 MB in bytes
        if image and image.size > max_size:
            raise ValidationError("Image size should not exceed 1 MB.")
        

          # Check if the file has a valid image extension
        allowed_extensions = ['.jpg', '.jpeg', '.png']
        if image and not any(image.name.lower().endswith(ext) for ext in allowed_extensions):
            raise ValidationError("Invalid file format. Please upload a .jpg, .jpeg, or .png file.")


        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        email = User.objects.normalize_email(email)
        dob = request.POST.get('dob')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, "Passowrd and confirm password must be same!")
            return HttpResponseRedirect(request.path_info)
        otp_obj = get_object_or_404(OTP, phone = phone, verified = True)
        otp_obj.delete()
        
        User.objects.create(phone = phone, email = email, date_of_birth = dob, first_name = first_name, last_name = last_name, image = image, password = make_password(password1))
        messages.success(request, "Account created successfully!")
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/createAccount.html', {"phone":phone})
    


    

@api_view(['POST'])
def pass_reset_email(request):
    phone  = request.data.get('phone')
    email  = request.data.get('email')
    
    if phone:
        user = get_object_or_404(User, phone = phone)
        return send_pass_reset_email(user)
    elif email:
        user = get_object_or_404(User, email = email)
        return send_pass_reset_email(user)
    else:
        return Response("data missing!", 400)
    
    
@api_view(['GET'])
def reset_pass_form(request, email, token):
    token_instance = PassResetToken.objects.filter(user__email = email, token = token).first()
    
    if token_instance:
        if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
            context = {
                'email':email,
                'token':token,
                # 'base_url':TEMPLATES_BASE_URL,
            }
            return render(request, 'accounts/new-pass-form.html', context)
        else:
            token_instance.delete()
            messages.error(request, 'Linked Expired')
            return redirect('alert')
    else:
        messages.info(request, "Instance Not found!")
        return redirect('alert')
    
@api_view(['POST'])
def reset_pass_confirm(request):
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    email = request.data.get('email')
    token = request.data.get('token')
    token_instance = PassResetToken.objects.filter(user__email = email, token = token).first()
    
    if token_instance:
        if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
            if password1 == password2:
                user = token_instance.user 
                user.password = make_password(password1)
                user.save()
                token_instance.delete()
                Token.objects.filter(user = user).delete()
                messages.success(request, "Password Updated successfully!")
                return redirect('alert')
            else:
                context = {
                'email':email,
                'token':token,
                'error': "Passowrd and confirm password must be same!",
                }
            return render(request, 'accounts/new-pass-form.html', context)
    
    else:
        messages.error(request, 'Linked Expired')
        return redirect('alert')









# @api_view(['POST'])
# def request_otp(request):
#     phone = request.data.get('phone')
    
#     if phone:
#         if User.objects.filter(phone = phone).exists():
#             return Response("Phone already exists!", status=400)
#         return send_otp(phone)    
    
#     else:
#         return Response("data_missing", status=400)


# @api_view(['POST'])
# def verify_otp(request):
#     phone = request.data.get('phone')
#     otp = request.data.get('otp')
    
#     otp_obj = get_object_or_404(OTP, phone = phone, verified = False)
    
#     if otp_obj.validity.replace(tzinfo=None) > datetime.datetime.utcnow():
#         if otp_obj.otp == int(otp):
#             otp_obj.verified = True 
#             otp_obj.save()
#             return Response("otp_verified_successfully!")
#         return Response("otp_not_matched!", status=400)
            
#     else:
#         return Response('otp_expired', status=400)

    

@api_view(['POST'])
def pass_reset_email(request):
    phone  = request.data.get('phone')
    email  = request.data.get('email')
    
    if phone:
        user = get_object_or_404(User, phone = phone)
        return send_pass_reset_email(user)
    elif email:
        user = get_object_or_404(User, email = email)
        return send_pass_reset_email(user)
    else:
        return Response("data missing!", 400)
    
    
@api_view(['GET'])
def reset_pass_form(request, email, token):
    token_instance = PassResetToken.objects.filter(user__email = email, token = token).first()
    
    if token_instance:
        if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
            context = {
                'email':email,
                'token':token,
                # 'base_url':TEMPLATES_BASE_URL,
            }
            return render(request, 'accounts/new-pass-form.html', context)
        else:
            token_instance.delete()
            messages.error(request, 'Linked Expired')
            return redirect('alert')
    else:
        messages.info(request, "Instance Not found!")
        return redirect('alert')
    
@api_view(['POST'])
def reset_pass_confirm(request):
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    email = request.data.get('email')
    token = request.data.get('token')
    token_instance = PassResetToken.objects.filter(user__email = email, token = token).first()
    
    if token_instance:
        if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
            if password1 == password2:
                user = token_instance.user 
                user.password = make_password(password1)
                user.save()
                token_instance.delete()
                Token.objects.filter(user = user).delete()
                messages.success(request, "Password Updated successfully!")
                return redirect('alert')
            else:
                context = {
                'email':email,
                'token':token,
                'error': "Passowrd and confirm password must be same!",
                }
            return render(request, 'accounts/new-pass-form.html', context)
    
    else:
        messages.error(request, 'Linked Expired')
        return redirect('alert')
    
@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def userdata(request):
    return Response()
# function to generate authentication token......

from rest_framework_simplejwt.tokens import RefreshToken
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class userLoginView(APIView):
    def post(self, request, format=None): 
        serializer = userLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True ):
            phone = serializer.data.get('phone')
            password = serializer.data.get('password')
            user = authenticate(phone = phone, password = password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'status': 200, 'token': token, 'message': 'Login success'}, status=status.HTTP_200_OK)
            return Response({'status': 400, 'message': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)
            

class userRegistrationView(APIView):

    def post(self, request, formate=None):

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'Message': 'User registered Successfully'},  status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class userProfielView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = userProfileViewSerializer(request.user)
        return Response(serializer.data)

class userPasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = userPasswordChangeSerializer(data = request.data, context = {'user' : request.user})
        if serializer.is_valid(raise_exception=True):
            return Response( {'message': 'Password changed Successfully!'}, status = status.HTTP_200_OK)
        return Response({'message': 'Error Occured!'}, status = status.HTTP_400_BAD_REQUEST)
        
class forgotPasswordEmailSend(APIView):
    def post(self, request, format = None):
        serializer = userForgotPasswordResetEmailSendSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password reset Email has been sent. Please check your Email'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class usePasswordResetVeiw(APIView):
    def post(self, request, uid, token, format=None):
        context = {'uid': uid, 'token': token}
        serializer = forgotPasswordReset(data=request.data, context = context)
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'password changed successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# celery code
from .tasks import loop

def test(request):
    loop.delay()
    return HttpResponse("celery testing...")


# To activate another terminal for celery task
# celery -A core.celery worker --pool=solo -l info