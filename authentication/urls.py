from django.urls import path
from . views import (
    UserRegistrationAPIView, VerifyUserRegistrationOtpAPIView,
    ResendUserRegistrationOtpAPIView
)


urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    
    path('verify/registration-otp/', VerifyUserRegistrationOtpAPIView.as_view(), name='verify-registration-otp'),
    
    path('resend/registration/otp/', ResendUserRegistrationOtpAPIView.as_view(), name='resend-registration-otp'),

]
