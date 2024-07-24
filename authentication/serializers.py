from rest_framework import serializers
from . models import User 
from . utils.otp import Otp
from .utils.email import send_email


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
        user = User.objects.create(**validated_data)
        otp = Otp.create_user_registration_otp(for_user=user)
        email_subject = 'Account Verification - (One Time Password) for Rest Auth'
        email_to = [user.email]
        email_body = f'Hi {user.username}. \n Below is the one time password for account verification. The otp will expire in 2 minutes. \n\n OPT: {otp}'
        data = {
            'email_subject': email_subject,
            'email_body': email_body,
            'email_to': email_to
        }
        send_email(data=data)
        
        return user 