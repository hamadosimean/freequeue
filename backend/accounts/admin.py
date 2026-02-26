from django.contrib import admin
from .models import CustomUser, OTP
from general_settings.constants import APP_NAME

admin.site.site_header = APP_NAME
admin.site.site_title = APP_NAME
admin.site.index_title = APP_NAME


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = (
        "country_code",
        "phone_number",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "is_superuser",
        "date_joined",
    )
    list_display_links = ("phone_number",)
    list_filter = (
        "country_code",
        "is_staff",
        "is_active",
    )
    search_fields = (
        "country_code",
        "phone_number",
    )
    ordering = ("-date_joined",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "country_code",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "email",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "password",
                )
            },
        ),
        ("Permissions", {"fields": ("groups",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "country_code",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "email",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "password",
                ),
            },
        ),
    )

    readonly_fields = ("date_joined",)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "code",
        "max_attempts",
        "locked_until",
        "is_verified",
        "used_at",
    )
    search_fields = (
        "user",
        "code",
        "is_verified",
    )
    list_display_links = (
        "user",
        "code",
        "is_verified",
    )
    list_filter = ("is_verified",)
    ordering = ("-used_at",)
    readonly_fields = (
        "used_at",
        "locked_until",
        "max_attempts",
        "is_verified",
        "code",
        "user",
    )
