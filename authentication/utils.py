from django.core.mail import EmailMessage
import uuid
from core.settings import TEMPLATES_BASE_URL
from rest_framework.response import Response
from .models import *
import random 
import datetime
from rest_framework.permissions import BasePermission
from django.template.loader import render_to_string




def send_otp(phone):
    otp = random.randint(1000, 9999)
    validity = datetime.datetime.now() + datetime.timedelta(minutes=10)
    OTP.objects.update_or_create(phone = phone, defaults={"otp":otp, "validity":validity, "verified":False})
    
    print(otp)
    return "opt send successfully!"


def new_token():
    token = uuid.uuid1().hex 
    print(token)
    return token

def token_response(user):
    token = new_token()
    Token.objects.create(token = token, user = user)
    return Response(f"token {token}")

    
def send_pass_reset_email(user):
    token = new_token()
    exp_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
    PassResetToken.objects.update_or_create(user = user, defaults={'user':user, 'token':token, 'validity':exp_time})
    
    email_data = {
        'token':token,
        'email':user.email, 
        'base_url':TEMPLATES_BASE_URL,
    }
    
    message = render_to_string('emails/reset_pass.html',  email_data)
    msg = EmailMessage('Reset Password', body=message, to=[user.email])
    msg.content_subtype = 'html'
    
    try:
        msg.send()
    except:
        pass  
    return Response("email_send_successfully")
    
class IsAuthenticatedUser(BasePermission):
    message = 'unauthenticated_user'
    
    def has_permission(self, request, view):
        return bool(request.user)