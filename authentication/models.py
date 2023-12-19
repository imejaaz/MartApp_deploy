from django.db import models
from .userManager import *
from django.contrib.auth.models import User, AbstractUser
import uuid
from django.contrib.auth import get_user_model

class cUser(AbstractUser):
    username =  None
    phone = models.CharField(unique=True, max_length=13)
    email = models.EmailField(max_length=50, unique=True)
    image = models.ImageField(upload_to='profile', null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.phone
        
User = get_user_model()
    
class OTP(models.Model):
    phone = models.CharField(max_length=9)
    otp = models.IntegerField()
    validity = models.DateTimeField()
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.phone
    
class Token(models.Model):
    token = models.CharField(max_length=5000) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Tokens_set')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.user.phone 
    
class PassResetToken(models.Model):
    token = models.CharField(max_length=5000) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pass_reset_tokens_set')
    validity = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.user.phone


