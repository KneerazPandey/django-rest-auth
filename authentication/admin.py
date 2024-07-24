from django.contrib import admin
from . models import User, UserRegistrationOtp, ForgetPasswordOtp


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'id', 'phone_number', 'first_name', 'last_name']
    

admin.site.register(UserRegistrationOtp)
admin.site.register(ForgetPasswordOtp)