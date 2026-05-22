from rest_framework import serializers
from .models import (
    Company,
    CompanyInfos,
    MarketingImage,
    MarketingVideo,
    Service,
    Queue,
    Payment,
    CompanySettings,
    Agent,
)

# ==============================================
# Company Serializers
# ==============================================


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "domain",
            "description",
            "logo",
            "address",
            "phone_number",
            "email",
            "website",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "is_active"]




# ===============================================
# Payment Serializers
# ==============================================


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "amount",
            "status",
            "transaction_id",
            "payment_method",
            "expired_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "expired_at"]


# ==============================================
# BranchAgent Serializers
# ==============================================


class AgentSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.UUIDField(write_only=True)
    user_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Agent
        fields = [
            "id",
            "company",
            "company_id",
            "user_id",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "is_active"]


# ==============================================
# CompanyInfos Serializers
# ==============================================


class CompanySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySettings
        fields = [
            "id",
            "is_voice_enabled",
            "voice_style",
            "allow_remote",
            "screen_mode",
            "show_info",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ===============================================
# Company Infos Serializers
# ==============================================


class CompanyInfosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfos
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ===============================================
# Marketing Image Serializers
# ==============================================


class MarketingImageSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = MarketingImage
        fields = [
            "company",
            "image",
            "title",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ===============================================
# MarketingVideo Serializers
# ==============================================


class MarketingVideoSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = MarketingVideo
        fields = [
            "id",
            "company",
            "video",
            "title",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ===============================================
# Service Serializers
# ==============================================


class ServiceSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "company",
            "name",
            "code",
            "description",
            "is_active",
            "daily_limit",
            "waiting_time",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ===============================================
# Queue Serializers
# ==============================================


class QueueSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Queue
        fields = [
            "id",
            "service",
            "status",
            "queue_number",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined"]
