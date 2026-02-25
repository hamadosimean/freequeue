from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class OTPVerifyThrottle(AnonRateThrottle):
    scope = "otp_verify"


class OTPSendThrottle(AnonRateThrottle):
    scope = "otp_send"


class AiThrottle(UserRateThrottle):
    scope = "ai"
