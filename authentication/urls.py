from django.urls import path
from .import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('alert/', views.alert, name='alert'),
    path('requestOtp/', views.requestOtp, name='requestOtp'),
    path('verifyOtp/<phone>', views.verifyOtp, name='verifyOtp'),
    path('createAccount/<phone>', views.createAccount, name='createAccount'),
    path('reset_pass_request/', views.pass_reset_email, name='pass_reset_email'),
    path('reset_pass_form/<email>/<token>/', views.reset_pass_form, name='reset_pass_form'),
    path('reset_pass_confirm/', views.reset_pass_confirm, name='reset_pass_confirm'),
    path('userdata/', views.userdata, name='userdata'),
    path('celery/', views.test, name='celery'),    
    # path('send_sms/', views.send_sms, name='send_sms'),
    
  
]+[
   
    path('login/', views.userLoginView.as_view(), name='login'),
    path('register/', views.userRegistrationView.as_view(), name='register'),
    path('profile/', views.userProfielView.as_view(),name= 'profile'),
    path('changePassword/', views.userPasswordChangeView.as_view(), name='changePassword'),
    path('forgotPassword/', views.forgotPasswordEmailSend.as_view(), name='forgotPassword'),
    path('reset_password/<uid>/<token>/', views.usePasswordResetVeiw.as_view(), name='forgotPassword'),

    


]+[
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
