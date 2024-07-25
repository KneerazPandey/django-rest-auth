from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        to=data['email_to']
    ) 
    email.send()
    return True


@shared_task
def delete_forget_password_otp_instance(instance_id):
    from . models import ForgetPasswordOtp
    try:
        instance = ForgetPasswordOtp.objects.get(id=instance_id)
        instance.delete()
    except ForgetPasswordOtp.DoesNotExist:
        pass 

    
@shared_task
def delete_registration_otp_instance(instance_id):
    from . models import UserRegistrationOtp
    try:
        instance = UserRegistrationOtp.objects.get(id=instance_id)
        instance.delete()
    except UserRegistrationOtp.DoesNotExist:
        pass 