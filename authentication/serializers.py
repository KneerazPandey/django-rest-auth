from rest_framework import serializers
from . models import User, ForgetPasswordOtp
from . utils.otp import Otp
from . task import send_email
from django.utils import timezone
import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=4, write_only=True)
    
    class Meta:
        model = User 
        fields = ['username', 'email', 'password']
    
    def validate(self, attrs: dict):
        username = attrs.get('username', '')
        
        if not username.isalnum():
            raise serializers.ValidationError('Username should only contain alphanumeric characters.')
        
        return super().validate(attrs)
        
    def create(self, validated_data: dict):
        user = User.objects.create_user(**validated_data)
        otp = Otp.create_user_registration_otp(for_user=user)
        email_subject = 'Account Verification - (One Time Password) for Rest Auth'
        email_to = [user.email]
        email_body = f'Hi {user.username}. \n Below is the one time password for account verification. The otp will expire in 2 minutes. \n\n OPT: {otp}'
        data = {
            'email_subject': email_subject,
            'email_body': email_body,
            'email_to': email_to
        }
        send_email.delay(data)
        
        return user 
    
    

class VerifyUserRegistrationOtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required=True)
    
    def validate(self, attrs: dict):
        from . models import UserRegistrationOtp
        
        otp_to_validate = attrs.get('otp', '')
        try:
            existing_otp = UserRegistrationOtp.objects.get(otp=otp_to_validate)
            if existing_otp.expired:
                raise serializers.ValidationError('Otp Expired. The otp you are using has already been expired.')
            current_date = timezone.now()
            existing_otp_expired_date = existing_otp.created_at + datetime.timedelta(minutes=3) #* After three minutes the OTP will expire
            if existing_otp_expired_date > current_date:
                if existing_otp.user.is_verified:
                    raise serializers.ValidationError('You have already verified your registration email.')
                return attrs 
            else:
                existing_otp.expired = True
                existing_otp.save()
                raise serializers.ValidationError('Your OTP has expired. Please ask new OTP for your registration.')
        except UserRegistrationOtp.DoesNotExist:
            raise serializers.ValidationError('Invalid Otp. The Otp you are using is not valid')
    
    

class ResendUserRegistrationOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    
    def validate(self, attrs: dict):
        from . models import UserRegistrationOtp
        
        email = attrs.get('email', '')
        try:
            user = User.objects.get(email=email)
            
            if user.is_verified:
                raise serializers.ValidationError('You have already verified your registration email. Not need to verified it twice.')
            
            #? Deleting all the other existing otp before sending the new one. As old otp no longer works
            otps = UserRegistrationOtp.objects.filter(user=user)
            otps.delete()
            
            otp = Otp.create_user_registration_otp(for_user=user)
            email_subject = 'Account Verification - (One Time Password) for Rest Auth'
            email_to = [user.email]
            email_body = f'Hi {user.username}. \n Below is the one time password for account verification. The otp will expire in 2 minutes. \n\n OPT: {otp}'
            data = {
                'email_subject': email_subject,
                'email_body': email_body,
                'email_to': email_to
            }
            send_email.delay(data)
            
            return super().validate(attrs) 
        except User.DoesNotExist:
            raise serializers.ValidationError('Cannot send the verification email as this email is not registered before.')
        
        

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=50, min_length=4, write_only=True)
        
    def validate(self, attrs: dict):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('Inalid email or password')
        if not user.is_verified:
            raise serializers.ValidationError("You haven't verified your email address. Please verified your email address first.")
        
        return super().validate(attrs)



class InitiateForgetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    
    def validate(self, attrs: dict):
        from . models import ForgetPasswordOtp
        try:
            user = User.objects.get(email=attrs.get('email', ''))
            
            #? Deleting all the previous OTP related to the user
            otps = ForgetPasswordOtp.objects.filter(user=user)
            otps.delete()
            
            otp = Otp.create_forget_password_otp(for_user=user)
            email_subject = 'Your one time password for Reseting Rest Auth Password'
            email_to = [user.email]
            email_body = f'Hi {user.username}. \n Below is the one time password for reseting your password. The otp will expire in 2 minutes. \n\n OPT: {otp}'
            data = {
                'email_subject': email_subject,
                'email_body': email_body,
                'email_to': email_to
            }
            send_email.delay(data)
            
            return super().validate(attrs)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email. This email is not registered in the system.')



class VerifyForgetPasswordOtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required=True)
    
    def validate(self, attrs: dict):
        from . models import ForgetPasswordOtp
        try:
            otp_to_validate = attrs.get('otp', 0)
            existing_otp = ForgetPasswordOtp.objects.get(otp=otp_to_validate)
            
            if existing_otp.expired:
                raise serializers.ValidationError('Otp Expired. The Otp you have used is already expired.')
            
            current_date = timezone.now()
            otp_expired_date = existing_otp.created_at + timezone.timedelta(minutes=3)
            if current_date > otp_expired_date:
                existing_otp.expired = True
                existing_otp.save()
                raise serializers.ValidationError('Otp Expired. The Otp you have used is already expired.') 
            authenticate(email=existing_otp.user.email, password=existing_otp.user.email)
            return super().validate(attrs)
        except Exception:
            raise serializers.ValidationError('Invalid Otp. The Otp you have used is either invalid or expired.')

    def get_otp_verified_user(self):
        '''This method should only vall ones the serializer is valid'''
        otp = self.validated_data.get('otp')
        existing_otp = ForgetPasswordOtp.objects.get(otp=otp)
        return existing_otp.user 


class ResetForgetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50, min_length=2, required=True)
    confirm_password = serializers.CharField(max_length=50, min_length=3, required=True)
    
    def validate(self, attrs: dict):
        password = attrs.get('password', '')
        confirm_password = attrs.get('confirm_password', '')
        if password == confirm_password:
            return super().validate(attrs)
        raise serializers.ValidationError('Password and Confirm Password must match')
    
    def get_user_after_resetting_password(self):
        '''This method only works ones the data is validated only'''
        request = self.context.get('request')
        user = request.user 
        user.set_password(self.validated_data.get('password'))
        user.save()
        return user 



class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=50, min_length=2, required=True)
    new_password = serializers.CharField(max_length=50, min_length=2, required=True)
    confirm_new_password = serializers.CharField(max_length=50, min_length=2, required=True)

    def validate(self, attrs: dict):
        try:
            current_password = attrs.get('current_password', '')
            new_password = attrs.get('new_password', '')
            confirm_new_password = attrs.get('confirm_new_password', '')
            request = self.context.get('request')
            user = request.user 
            
            if new_password != confirm_new_password:
                raise serializers.ValidationError('New password and confirm password does not match')
            if not check_password(current_password, user.password):
                raise serializers.ValidationError('The current password does not match')
            
            return super().validate(attrs)
        except Exception:
            raise serializers.ValidationError('Error occured while changing password. Please try again.')
    
    def change_password(self):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()
        return user 
    

class UserResponseSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tokens = serializers.DictField(read_only=True)
    
    class Meta:
        model = User 
        fields = '__all__'