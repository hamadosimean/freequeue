from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from . import views

urlpatterns = [
    path("otp/send", views.SendOTPAPIView.as_view(), name="send-otp"),
    path("otp/verify", views.VerifyOTPAPIView.as_view(), name="verify-otp"),
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("settings", views.UserSettingsAPIView.as_view(), name="user-settings"),
    path("contact", views.ContactAPIView.as_view(), name="contact"),
]
