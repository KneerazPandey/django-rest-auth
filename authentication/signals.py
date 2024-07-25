from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import ForgetPasswordOtp, UserRegistrationOtp
from . task import delete_forget_password_otp_instance, delete_registration_otp_instance


@receiver(post_save, sender=ForgetPasswordOtp)
def schedule_delete_forget_password_instance(sender, instance, created, **kwargs):
    if created:
        delete_forget_password_otp_instance.apply_async((instance.id,), countdown=180)


@receiver(post_save, sender=UserRegistrationOtp)
def schedule_delete_registration_otp_instance(sender, instance, created, **kwargs):
    if created:
        delete_registration_otp_instance.apply_async((instance.id,), countdown=180)