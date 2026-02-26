from django.contrib import admin
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
    list_display = ["branch", "amount", "status", "payment_method"]
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
    list_display = ["title", "branch"]
    list_filter = ["branch"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["title", "branch"]
    list_filter = ["branch"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "branch", "is_active"]
    list_filter = ["branch", "is_active"]
    search_fields = ["name", "description"]
    ordering = ["-created_at"]


@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ["service", "user", "status", "queue_number"]
    list_filter = ["service", "user", "status"]
    search_fields = ["service__name", "user__username"]
    ordering = ["-created_at"]
