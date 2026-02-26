from django.utils.timezone import timedelta
from .admin_ui import *
from .base import env
import os
from .db import *
from .installed_apps import *
from .middleware import *
from .static_settings import *

# restframework settings

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # rate limite
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",
        "user": "1000/day",
        "send_otp": "10/minute",
        "verify_otp": "10/minute",
    },
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# JWT Token
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}


# Email settings
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("EMAIL_HOST_USER")

# Authentication settings
AUTH_USER_MODEL = "accounts.CustomUser"
AUTHENTICATION_BACKENDS = [
    "accounts.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]
# Djoser setup
DJOSER = {
    "USER_ID_FIELD": "id",
    "LOGIN_FIELD": "email",
    "SEND_ACTIVATION_EMAIL": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "JWT_AUTH": True,
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/?uid={uid}&token={token}",
    "USERNAME_RESET_CONFIRM_URL": "username/reset/confirm/?uid={uid}&token={token}",
    "ACTIVATION_URL": "activate/?uid={uid}&token={token}",
    "SERIALIZERS": {
        "user_create": "accounts.serializers.CustomUserCreateSerializer",
        "user": "accounts.serializers.CustomUserSerializer",
        "current_user": "accounts.serializers.CustomUserSerializer",
    },
}


# Cors settings
CORS_ALLOWED_ORIGINS = [
    f"http://{host}:{env.int('APP_PORT')}" for host in env.list("ALLOWED_HOSTS")
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS


# celery setup worker
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = env.list("CELERY_ACCEPT_CONTENT")
CELERY_TASK_SERIALIZER = env("CELERY_TASK_SERIALIZER")
CELERY_RESULT_SERIALIZER = env("CELERY_RESULT_SERIALIZER")
CELERY_TIMEZONE = env("CELERY_TIMEZONE")
CELERY_ENABLE_UTC = env.bool("CELERY_ENABLE_UTC")
CELERY_TASK_TRACK_STARTED = env.bool("CELERY_TASK_TRACK_STARTED")
CELERY_BEAT_SCHEDULER = env("CELERY_BEAT_SCHEDULER")


# Log settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "json": {
            "format": '{"level": "%(levelname)s", "time": "%(asctime)s", "module": "%(module)s", "message": "%(message)s"}',
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "backend.log"),
            "maxBytes": 1024 * 1024 * 15,
            "backupCount": 10,
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "accounts": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")


SPECTACULAR_SETTINGS = {
    "TITLE": "FreeQueues API",
    "DESCRIPTION": "FreeQueues API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}
