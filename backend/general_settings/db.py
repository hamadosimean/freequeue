from .base import env

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}

# redis setup cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://:{env('REDIS_PASSWORD')}@{env('REDIS_HOST')}:{env('REDIS_PORT')}/{env('REDIS_DB')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "CONNECTION_POOL_CLASS": "redis.BlockingConnectionPool",
        "CONNECTION_POOL_CLASS_KWARGS": {
            "max_connections": 50,
            "timeout": 20,
        },
        "KEY_PREFIX": "freequeues",
        "TIMEOUT": 300,
    }
}

# Store sessions in Redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CACHE_TTL = env("CACHE_TTL")
