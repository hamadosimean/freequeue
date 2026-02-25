INSTALLED_APPS = [
    # apps insatalled
    "django_prometheus",
    "rest_framework",
    "djoser",
    "corsheaders",
    "django_celery_beat",
    "whitenoise",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_filters",
    "channels",
    # health check
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    # local apps
    "accounts",
    "stats",
    "core",
    "assistant",
]
