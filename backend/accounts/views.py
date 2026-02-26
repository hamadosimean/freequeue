# Standard library
from django.db import transaction
import logging
import secrets
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model

# Third-party
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


# local
from .models import OTP, CustomUser
from .utils import send_otp
from .serializers import (
    SendOTPSerializer,
    VerifyOTPSerializer,
)
from general_settings.throttles import OTPVerifyThrottle, OTPSendThrottle
from general_settings.constants import OTP_MAX_ATTEMPTS
# Create your views here.

logger = logging.getLogger(__name__)

User = get_user_model()


class SendOTPAPIView(APIView):
    """
    View to handle OTP generation and sending.

    This view accepts a phone number, checks if it is registered in the system,
    and if so, generates and sends an OTP via SMS (using Kannel).
    It handles both creating new users (if not exists in CustomUser but exists in Abonne)
    and updating existing OTP records.
    """

    throttle_classes = [OTPSendThrottle]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        country_code = serializer.validated_data["country_code"]

        # check if phone number is registered
        user = CustomUser.objects.filter(
            phone_number=phone_number, country_code=country_code
        ).first()
        if not user:
            return Response(
                {"detail": _("Phone number not registered")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # OTP generation
        otp_code = "".join([str(secrets.randbelow(10)) for _ in range(6)])

        # save or update OTP
        try:
            with transaction.atomic():
                phone_otp, created = OTP.objects.update_or_create(
                    user=user,
                    is_verified=False,
                    defaults={
                        "code": make_password(otp_code),
                        "used_at": None,
                        "max_attempts": 0,
                    },
                )
                # send OTP
                otp, send_status = send_otp(country_code + phone_number, otp=otp_code)
                if not send_status.get("success", False):
                    logger.error(
                        _("OTP send failed"),
                        extra={
                            "phone_number": phone_number,
                            "error": str(send_status),
                            "status": send_status,
                        },
                    )
                    raise Exception(f"Failed to send OTP: {send_status.get('message')}")

        except Exception as e:
            logger.error(
                _("Error saving OTP"),
                extra={
                    "phone_number": phone_number,
                    "error": str(e),
                },
            )
            return Response(
                {"detail": _("Unable to send OTP. Please try again later.")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"detail": f"OTP sent to {phone_number}"},
            status=status.HTTP_200_OK,
        )


class VerifyOTPAPIView(APIView):
    """
    View to verify the OTP provided by the user.

    This view accepts a phone number and an OTP. It verifies the OTP against
    the stored hash. If valid and not expired, it marks the OTP as verified
    and returns JWT access and refresh tokens.
    """

    permission_classes = [AllowAny]
    throttle_classes = [OTPVerifyThrottle]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data["phone_number"]
            code = serializer.validated_data["code"]

        try:
            phone_otp = OTP.objects.filter(
                user__phone_number=phone_number, is_verified=False
            ).latest("created_at")
        except OTP.DoesNotExist:
            return Response(
                {"detail": _("Phone number not found or OTP not requested")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            # Check if account is locked
            if phone_otp.is_locked():
                return Response(
                    {"detail": _("Too many failed attempts. Try again later.")},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )

            # Check if OTP expired
            if phone_otp.is_expired():
                return Response(
                    {"detail": _("OTP has expired. Please request a new one")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if already verified
            if phone_otp.is_verified:
                return Response(
                    {"detail": _("OTP already verified. Please request a new one")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Verify OTP
            if check_password(code, phone_otp.code):
                # Successful verification
                phone_otp.is_verified = True
                phone_otp.max_attempts = 0
                phone_otp.used_at = timezone.now()
                phone_otp.save()

                # Activate user after successful OTP verification
                if not phone_otp.user.is_active:
                    phone_otp.user.is_active = True
                    phone_otp.user.save()

                # Generate tokens
                return Response(
                    {"detail": "OTP verified successfully"}, status=status.HTTP_200_OK
                )

            # Invalid OTP - increment attempts
            phone_otp.max_attempts += 1
            if phone_otp.max_attempts >= OTP_MAX_ATTEMPTS:
                phone_otp.locked_until = timezone.now() + timezone.timedelta(minutes=30)
            phone_otp.save()

            return Response(
                {"detail": _("Invalid OTP")}, status=status.HTTP_400_BAD_REQUEST
            )
