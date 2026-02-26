from rest_framework import serializers
from .models import (
    Company,
    Branch,
    BranchInfos,
    MarketingImage,
    Video,
    Service,
    Queue,
    Payment,
    BranchSettings,
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


# ==============================================
# Branch Serializers
# ==============================================


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = [
            "id",
            "name",
            "description",
            "address",
            "phone_number",
            "email",
            "website",
            "is_active",
            "is_opened",
            "opening_time",
            "closing_time",
            "long",
            "lat",
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
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ==============================================
# BranchInfos Serializers
# ==============================================


class BranchSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchSettings
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
# Branch Infos Serializers
# ==============================================


class BranchInfosSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchInfos
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
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MarketingImage
        fields = [
            "id",
            "branch",
            "branch_id",
            "image",
            "title",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ===============================================
# Video Serializers
# ==============================================


class VideoSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Video
        fields = [
            "id",
            "branch",
            "branch_id",
            "video",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ===============================================
# Service Serializers
# ==============================================


class ServiceSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "branch",
            "branch_id",
            "name",
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
    service_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Queue
        fields = [
            "id",
            "service",
            "service_id",
            "status",
            "queue_number",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
