import secrets


class Otp:
    @staticmethod
    def create_user_registration_otp(for_user) -> int:
        from authentication.models import UserRegistrationOtp
        
        registration_otps = UserRegistrationOtp.objects.all()
        otp = Otp._create_otp(registration_otps)
        UserRegistrationOtp.objects.create(user=for_user, otp=otp)
        return otp 
    
    @staticmethod
    def create_forget_password_otp(for_user) -> int:
        from authentication.models import ForgetPasswordOtp
        
        forget_password_otps = ForgetPasswordOtp.objects.all()
        otp = Otp._create_otp(forget_password_otps)
        ForgetPasswordOtp.objects.create(user=for_user, otp=otp)
        return otp
    
    @staticmethod
    def _create_otp(queryset) -> int:
        while True:
            otp = int(''.join([ str(secrets.randbelow(10)) for _ in range(6)]))
            if not queryset:
                return otp
            
            for registration_otp in queryset:
                if registration_otp.otp != otp:
                    return otp
    