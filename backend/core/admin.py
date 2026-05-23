from django.contrib import admin
from .models import (
    Company,
    Agent,
    CompanyInfos,
    MarketingImage,
    MarketingVideo,
    Service,
    Queue,
    Payment,
    CompanySettings,
)

# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "domain",
        "is_active",
        "is_opened",
        "opening_time",
        "closing_time",
        "long",
        "lat",
    ]
    list_filter = ["domain", "is_active", "is_opened"]
    search_fields = ["name", "description"]
    ordering = ["-created_at"]


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ["user__email", "is_active"]
    list_filter = ["user__email", "is_active"]
    search_fields = ["user__email"]
    ordering = ["-created_at"]
    search_fields = ["company__name", "user__email"]
    ordering = ["-created_at"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "amount",
        "status",
        "payment_method",
        "expired_at",
        "transaction_id",
    ]
    list_filter = ["company", "status", "payment_method"]
    search_fields = ["company__name", "transaction_id"]
    ordering = ["-created_at"]


@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "is_voice_enabled",
        "voice_style",
        "allow_remote",
        "screen_mode",
        "show_info",
    ]
    list_filter = [
        "company",
        "is_voice_enabled",
        "voice_style",
        "allow_remote",
        "screen_mode",
    ]
    search_fields = ["company__name", "voice_style", "screen_mode"]
    ordering = ["-created_at"]


@admin.register(CompanyInfos)
class CompanyInfosAdmin(admin.ModelAdmin):
    list_display = ["title", "company"]
    list_filter = ["company"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]


@admin.register(MarketingImage)
class MarketingImageAdmin(admin.ModelAdmin):
    list_display = ["id", "company", "image", "created_at", "updated_at"]
    list_filter = ["company"]
    list_links = ["id", "title"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]


@admin.register(MarketingVideo)
class MarketingVideoAdmin(admin.ModelAdmin):
    list_display = ["id", "company", "title", "video", "created_at", "updated_at"]
    list_filter = ["company"]
    list_links = ["id", "title"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "company",
        "name",
        "code",
        "daily_limit",
        "waiting_time",
        "is_active",
    ]
    list_filter = ["company", "is_active"]
    list_links = [
        "id",
        "name",
    ]
    search_fields = ["company__name", "name", "description"]
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
