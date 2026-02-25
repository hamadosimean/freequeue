from django.contrib.auth.backends import BaseBackend

from django.contrib.auth import get_user_model

User = get_user_model()


class PhoneBackend(BaseBackend):
    """
    Authenticate users using phone_number only (passwordless).
    Typically used with OTP verification.
    """

    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        if phone_number is None:
            phone_number = kwargs.get("username")
        if password is None:
            password = kwargs.get("password")
        try:
            user = User.objects.get(phone_number=phone_number, password=password)
            if user.is_active:
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
