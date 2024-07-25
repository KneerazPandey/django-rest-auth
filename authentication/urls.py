from django.urls import path
from . views import (
    UserRegistrationAPIView, VerifyUserRegistrationOtpAPIView,
    ResendUserRegistrationOtpAPIView, UserLoginAPIView, 
    InitiateForgetPasswordRequestAPIView, VerifyForgetPasswordOtpAPIView,
    ResetForgetPasswordAPIView
)


urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    
    path('verify/registration-otp/', VerifyUserRegistrationOtpAPIView.as_view(), name='verify-registration-otp'),
    
    path('resend/registration-otp/', ResendUserRegistrationOtpAPIView.as_view(), name='resend-registration-otp'),
    
    path('login', UserLoginAPIView.as_view(), name='login'),
    
    path('initiate/forget-password/', InitiateForgetPasswordRequestAPIView.as_view(), name='initiate-forget-password'),
    
    path('verify/forget-password-otp/', VerifyForgetPasswordOtpAPIView.as_view(), name='verify-forget-password-otp'),
    
    path('reset/forget-password/', ResetForgetPasswordAPIView.as_view(), name='reset-forget-password'),

]
