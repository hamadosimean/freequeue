# App settings
APP_NAME = "Free Queues"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = (
    "Free Queues is a platform that allows you to create and manage queues."
)
APP_AUTHOR = "Hamado Simean"

# Cache settings
CACHE_TTL = 7

# OTP settings
OTP_EXPIRATION_TIME = 60
OTP_MAX_ATTEMPTS = 3

# Company domains
COMPANY_DOMAINS = (
    ("health", "Health"),
    ("education", "Education"),
    ("governement", "Governement"),
    ("technology", "Technology"),
    ("banking", "Banking"),
    ("transport", "Transport"),
    ("hotel", "Hotel"),
    ("restaurant", "Restaurant"),
    ("shopping", "Shopping"),
    ("other", "Other"),
)


QUEUE_STATUS = (
    ("waiting", "Waiting"),
    ("called", "Called"),
    ("served", "Served"),
    ("canceled", "Canceled"),
)

PAYMENT_STATUS = (
    ("pending", "Pending"),
    ("paid", "Paid"),
    ("failed", "Failed"),
    ("expired", "Expired"),
)

PAYMENT_METHOD = (
    ("cash", "Cash"),
    ("card", "Card"),
    ("mobile_money", "Mobile Money"),
    ("other", "Other"),
)

VOICE_STYLE = (
    ("man", "Man"),
    ("woman", "Woman"),
    ("child", "Child"),
    ("elderly", "Elderly"),
)

SCREEN_MODE = (
    ("1", "Screen 1"),
    ("2", "Screen 2"),
    ("3", "Screen 3"),
)
