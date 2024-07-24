from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from . serializers import (
    UserRegistrationSerializer, VerifyUserRegistrationOtpSerializer, 
    ResendUserRegistrationOtpSerializer
)
from . models import (
    UserRegistrationOtp
)



class UserRegistrationAPIView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class VerifyUserRegistrationOtpAPIView(generics.GenericAPIView):
    serializer_class = VerifyUserRegistrationOtpSerializer
    permission_classes = [AllowAny]
    
    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data.get('otp')
            registration_otp = UserRegistrationOtp.objects.get(otp=otp) #* This will definately get the object because it is already validated in serializer side.
            registration_otp.user.is_verified = True
            registration_otp.user.save()
            data = {
                    'success': 'Your OTP Verified sucessfully',
                    'tokens': registration_otp.user.tokens(),
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
class ResendUserRegistrationOtpAPIView(generics.GenericAPIView):
    serializer_class = ResendUserRegistrationOtpSerializer
    permission_classes = [AllowAny]
    
    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data) 
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            return Response(data={'success': f'The new email verification opt has been sent to your email address: {email}'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)