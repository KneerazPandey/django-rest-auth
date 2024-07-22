from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from authentication.managers import AuthenticationUserManager
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    password = models.CharField(max_length=50)
    phone_number = PhoneNumberField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, null=True, default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    
    objects = AuthenticationUserManager()
    
    def __str__(self) -> str:
        return self.email
    