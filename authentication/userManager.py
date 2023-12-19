from django.contrib.auth.models import BaseUserManager
from django.http import HttpResponse


class UserManager(BaseUserManager):

    def create_user(self, phone, email, password=None, password2=None,  **extra):
        if not phone:
            raise ValueError('Phone number is required here')
        if not email:
            raise ValueError('Email is required here')    
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password=None, **extra):

        user = self.create_user(phone,email=email,  password=password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user