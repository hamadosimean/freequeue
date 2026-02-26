from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.utils.translation import gettext_lazy as _

User = get_user_model()


# User serializer
class CustomUserCreateSerializer(UserCreateSerializer):
    """Custom user create serializer"""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "password",
        )
        extra_kwargs = {
            "email": {
                "required": True,
            },
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
            },
        }


class CustomUserSerializer(UserSerializer):
    """Custom user serializer"""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "date_joined",
            "last_login",
        )
        read_only_fields = ["id"]


# OTP send serializer
class SendOTPSerializer(serializers.Serializer):
    """Serializer for sending OTP."""

    phone_number = serializers.RegexField(
        regex=r"^\+?[0-9]{8,15}$",
        max_length=20,
        error_messages={"invalid": _("Enter a valid phone number (8-15 digits).")},
    )
    country_code = serializers.CharField(
        max_length=6,
        error_messages={"invalid": _("Enter a valid country code (6 digits).")},
    )

    def validate_country_code(self, value):
        if not value:
            return "+226"
        return value


# OTP verify serializer
class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(regex=r"^\+?[0-9]{8,15}$", max_length=20)
    code = serializers.RegexField(
        regex=r"^[0-9]{6}$",
        error_messages={"invalid": _("OTP must be exactly 6 digits.")},
    )
