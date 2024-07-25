from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from . serializers import (
    UserRegistrationSerializer, VerifyUserRegistrationOtpSerializer, 
    ResendUserRegistrationOtpSerializer, UserLoginSerializer, UserResponseSerializer,
    InitiateForgetPasswordRequestSerializer, VerifyForgetPasswordOtpSerializer, 
    ResetForgetPasswordSerializer, ChangePasswordSerializer
)
from . models import (
    UserRegistrationOtp, User
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
    


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data.get('email'))
            response = UserResponseSerializer(user).data
            
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_200_OK)
    


class InitiateForgetPasswordRequestAPIView(generics.GenericAPIView):
    serializer_class = InitiateForgetPasswordRequestSerializer
    permission_classes = [AllowAny]
    
    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            data = {
                'success': 'The forget password OTP has been sent successfully to your email address.',
                'email': email
            }  
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyForgetPasswordOtpAPIView(generics.GenericAPIView):
    serializer_class = VerifyForgetPasswordOtpSerializer
    permission_classes = [AllowAny]
    
    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.get_otp_verified_user()
            data = UserResponseSerializer(user).data
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    

class ResetForgetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetForgetPasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.get_user_after_resetting_password()
            data = UserResponseSerializer(user).data
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    

class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class= ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request: Request, *args, **kwargs):
        context = {
            'request': request
        }
        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid():
            serializer.change_password()
            data = UserResponseSerializer(request.user).data
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    