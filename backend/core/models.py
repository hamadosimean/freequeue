import datetime
from django.template.defaultfilters import default
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from general_settings.utils import TimeStampedModel
from django.contrib.auth import get_user_model
from django.utils import timezone
from general_settings.constants import (
    COMPANY_DOMAINS,
    QUEUE_STATUS,
    PAYMENT_STATUS,
    PAYMENT_METHOD,
    VOICE_STYLE,
    SCREEN_MODE,
)

User = get_user_model()
# Create your models here.


# ======================================
# Company model
# ======================================
class Company(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="company",
        verbose_name=_("User"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    domain = models.CharField(
        max_length=100,
        choices=COMPANY_DOMAINS,
        default="other",
        verbose_name=_("Domain"),
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    logo = models.ImageField(
        upload_to="company_logos/", blank=True, null=True, verbose_name=_("Logo")
    )
    address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Address")
    )
    phone_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_("Phone number")
    )
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email"))
    website = models.URLField(blank=True, null=True, verbose_name=_("Website"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    def __str__(self):
        return self.user.get_full_name() + " - " + self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["domain"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_company_name",
            ),
        ]




# ============================================
# Company Agents
# ============================================


class Agent(TimeStampedModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="agent",
        verbose_name=_("Company"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="agent",
        verbose_name=_("User"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    def __str__(self):
        return self.company.name + " - " + self.user.get_full_name()

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["user"]),
            models.Index(fields=["is_active"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "user"],
                name="unique_agent",
            ),
        ]


# =============================================
# Payment model
# =============================================
class Payment(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="payment",
        verbose_name=_("Company"),
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, verbose_name=_("Amount")
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="pending",
        verbose_name=_("Status"),
    )
    transaction_id = models.CharField(max_length=100, verbose_name=_("Transaction ID"))
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD,
        default="cash",
        verbose_name=_("Payment method"),
    )
    expired_at = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(days=7),
        verbose_name=_("Expiration date"),
    )

    def __str__(self):
        return self.company.name + " - " + self.transaction_id

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["company"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "transaction_id"],
                name="unique_transaction",
            ),
            models.CheckConstraint(
                check=models.Q(amount__gte=0),
                name="amount_gte_0",
            ),
        ]


# =======================================
# Company settings model
# ========================================
class CompanySettings(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="setting",
        verbose_name=_("Company"),
    )
    is_voice_enabled = models.BooleanField(
        default=True, verbose_name=_("Voice enabled")
    )
    voice_style = models.CharField(
        max_length=20,
        choices=VOICE_STYLE,
        default="natural",
        verbose_name=_("Voice style"),
    )
    allow_remote = models.BooleanField(default=True, verbose_name=_("Allow remote"))
    screen_mode = models.CharField(
        max_length=20,
        choices=SCREEN_MODE,
        default="1",
        verbose_name=_("Screen mode"),
    )
    show_info = models.BooleanField(default=True, verbose_name=_("Show info"))

    def __str__(self):
        return self.company.name + " - " + self.screen_mode

    class Meta:
        verbose_name = "Company Settings"
        verbose_name_plural = "Company Settings"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["company"]),
        ]


# ======================================
# Company Infos model
# ======================================
class CompanyInfos(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="infos",
        verbose_name=_("Company"),
    )
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    def __str__(self):
        return self.company.name + " - " + self.title

    class Meta:
        verbose_name = "Company Info"
        verbose_name_plural = "Company Infos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["company"]),
        ]


class MarketingImage(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="image",
        verbose_name=_("Company"),
    )
    image = models.ImageField(upload_to="marketing_images/", verbose_name=_("Image"))
    title = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("Title")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    def __str__(self):
        return self.company.name + " - " + self.title

    class Meta:
        verbose_name = "Marketing Image"
        verbose_name_plural = "Marketing Images"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["company"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "title"],
                name="unique_marketing_image_company_title",
            ),
        ]


# ===================================================
# Video model
# ===================================================
class MarketingVideo(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="video",
        verbose_name=_("Company"),
    )
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    video = models.FileField(upload_to="videos/", verbose_name=_("Video"))

    def __str__(self):
        return self.company.name + " - " + self.title

    class Meta:
        verbose_name = "Marketing Video"
        verbose_name_plural = "Marketing Videos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["company"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "title"],
                name="unique_marketing_video_company_title",
            ),
        ]


# ===================================================
#  Service model
# ===================================================
class Service(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="service",
        verbose_name=_("Company"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    # TODO: add code service that will be use for generate ticket
    code = models.CharField(max_length=10, verbose_name=_("Code"), unique=True)
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    daily_limit = models.IntegerField(default=2000, verbose_name=_("Daily limit"))
    waiting_time = models.IntegerField(
        default=10, verbose_name=_("Wait time (minutes)")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    def __str__(self):
        return self.company.name + " - " + self.name

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["company"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_service_company_name",
            ),
            models.UniqueConstraint(
                fields=["code"],
                name="unique_service_code",
            ),
        ]


# ========================================================
# Queue model
# ========================================================
class Queue(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="queue",
        verbose_name=_("Service"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="queue",
        verbose_name=_("User"),
    )
    status = models.CharField(
        max_length=20,
        choices=QUEUE_STATUS,
        default="waiting",
        verbose_name=_("Status"),
    )
    queue_number = models.IntegerField(default=1, verbose_name=_("Queue number"))
    date_joined = models.DateField(
        verbose_name=_("Date joined"), default=datetime.date.today
    )

    def __str__(self):
        return self.service.name + " - " + self.user.get_full_name()

    class Meta:
        verbose_name = "Queue"
        verbose_name_plural = "Queues"
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["service"]),
            models.Index(fields=["date_joined"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(queue_number__gte=1),
                name="queue_number_gte_1",
            ),
        ]
