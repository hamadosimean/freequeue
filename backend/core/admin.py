from django.contrib import admin
from .models import (
    Company,
    Branch,
    BranchInfos,
    MarketingImage,
    MarketingVideo,
    Service,
    Queue,
    Payment,
    BranchSettings,
)

# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "domain", "is_active"]
    list_filter = ["domain", "is_active"]
    search_fields = ["name", "description"]
    ordering = ["-created_at"]


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ["name", "company", "is_active", "is_opened"]
    list_filter = ["company", "is_active", "is_opened"]
    search_fields = ["name", "description"]
    ordering = ["-created_at"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "branch",
        "amount",
        "status",
        "payment_method",
        "expired_at",
        "transaction_id",
    ]
    list_filter = ["branch", "status", "payment_method"]
    search_fields = ["branch__name", "transaction_id"]
    ordering = ["-created_at"]


@admin.register(BranchSettings)
class BranchSettingsAdmin(admin.ModelAdmin):
    list_display = [
        "branch",
        "is_voice_enabled",
        "voice_style",
        "allow_remote",
        "screen_mode",
        "show_info",
    ]
    list_filter = [
        "branch",
        "is_voice_enabled",
        "voice_style",
        "allow_remote",
        "screen_mode",
    ]
    search_fields = ["branch__name", "voice_style", "screen_mode"]
    ordering = ["-created_at"]


@admin.register(BranchInfos)
class BranchInfosAdmin(admin.ModelAdmin):
    list_display = ["title", "branch"]
    list_filter = ["branch"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]


@admin.register(MarketingImage)
class MarketingImageAdmin(admin.ModelAdmin):
    list_display = ["id", "branch", "image", "created_at", "updated_at"]
    list_filter = ["branch"]
    list_links = ["id", "title"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]


@admin.register(MarketingVideo)
class MarketingVideoAdmin(admin.ModelAdmin):
    list_display = ["id", "branch", "title", "video", "created_at", "updated_at"]
    list_filter = ["branch"]
    list_links = ["id", "title"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "branch",
        "name",
        "daily_limit",
        "waiting_time",
        "is_active",
    ]
    list_filter = ["branch", "is_active"]
    list_links = [
        "id",
        "name",
    ]
    search_fields = ["name", "description"]
    ordering = ["-created_at"]


@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ["id", "service", "user", "status", "queue_number", "date_joined"]
    list_filter = ["service", "user", "status", "date_joined"]
    list_links = [
        "id",
        "service",
    ]
    search_fields = ["service__name", "user__username"]
    ordering = ["-date_joined"]
