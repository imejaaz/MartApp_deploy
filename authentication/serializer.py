from rest_framework import serializers
from .models import cUser
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField( style = {'input_type':'password'}, write_only = True)
    class Meta:
        model = cUser
        fields = ['phone', 'email', 'password', 'password2']
                  

    def validate(self, attrs):
        password1 = attrs['password']
        password2 = attrs['password2']
        print("Password1:", password1)
        print("Password2:", password2)

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError("Your entered passwords doesn't match!")
        
        max_size = 3 * 1024 * 1024  # 3 MB in bytes        
        image = attrs.get('image')
        if image and image.size > max_size:
            raise serializers.ValidationError("Image size should not exceed 1 MB.")
        
          # Check if the file has a valid image extension
        allowed_extensions = ['.jpg', '.jpeg', '.png']
        if image and not any(image.name.lower().endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError("Invalid file format. Please upload a .jpg, .jpeg, or .png file.")
        
        return super().validate(attrs)


    def create(self, validated_data):
       
        return cUser.objects.create_user(**validated_data)

class userLoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=100)
    class Meta:
        model = cUser
        fields = ['phone', 'password']

class userProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
      model = cUser
      fields = ['first_name','last_name', 'phone', 'email', 'date_of_birth', 'image', 'last_login']

class userPasswordChangeSerializer(serializers.Serializer):
    
    password = serializers.CharField( max_length = 100, write_only = True, style = {'input_type':'password'})
    password2 = serializers.CharField(max_length = 100, write_only = True, style = {'input_type':'password'})

    class Meta:
        fields = ['password', 'password2']
    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password Does not match!')
        user.set_password(password)
        user.save()
        return attrs

class userForgotPasswordResetEmailSendSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 100)
    class Meta:
        fields = ['email']
    def validate(self, attrs):
        email = attrs.get('email')
        if cUser.objects.filter(email = email).exists():
            user = cUser.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://127.0.0.1:8000/auth/reset_password/'+uid+'/'+token
            print(user.first_name, uid, token, link)
            return attrs

        else:
            raise serializers.ValidationError('Your entered email is not registered!')
class forgotPasswordReset(serializers.Serializer):
    password = serializers.CharField( max_length = 100, write_only = True, style = {'input_type':'password'})
    password2 = serializers.CharField(max_length = 100, write_only = True, style = {'input_type':'password'})
    class Meta:
        fields = ['password', 'password2']
    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        
        uid = self.context.get('uid')
        token = self.context.get('token')
       
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password Does not match!')
        
        uid = smart_str(urlsafe_base64_decode(uid))
        user = cUser.objects.get(id = uid)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError('Invalid token or expired!')
        user.set_password(password)
        user.save()
        return attrs