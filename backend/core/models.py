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


# ======================================
# branch model
# ======================================
class Branch(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="branch",
        verbose_name=_("Company"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Address")
    )
    phone_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_("Phone number")
    )
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email"))
    website = models.URLField(blank=True, null=True, verbose_name=_("Website"))
    is_active = models.BooleanField(default=False, verbose_name=_("Is active"))
    is_opened = models.BooleanField(default=True, verbose_name=_("Is opened"))
    opening_time = models.TimeField(
        blank=True, null=True, verbose_name=_("Opening time")
    )
    closing_time = models.TimeField(
        blank=True, null=True, verbose_name=_("Closing time")
    )
    long = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name=_("Longitude"),
    )
    lat = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name=_("Latitude"),
    )

    def __str__(self):
        return self.company.user.get_full_name() + " - " + self.name

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["company"]),
            models.Index(fields=["is_opened"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_branch_name",
            ),
        ]


# ============================================
# Branch Agents
# ============================================


class BranchAgent(TimeStampedModel):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_agent",
        verbose_name=_("Branch"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="branch_agent",
        verbose_name=_("User"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    def __str__(self):
        return self.branch.name + " - " + self.user.get_full_name()

    class Meta:
        verbose_name = "Branch Agent"
        verbose_name_plural = "Branch Agents"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["branch"]),
            models.Index(fields=["user"]),
            models.Index(fields=["is_active"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["branch", "user"],
                name="unique_branch_agent",
            ),
        ]


# =============================================
# Payment model
# =============================================
class Payment(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="payment",
        verbose_name=_("Branch"),
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
        return self.branch.name + " - " + self.transaction_id

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["branch"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["branch", "transaction_id"],
                name="unique_transaction",
            ),
            models.CheckConstraint(
                check=models.Q(amount__gte=0),
                name="amount_gte_0",
            ),
        ]


# =======================================
# Branch settings model
# ========================================
class BranchSettings(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    branch = models.OneToOneField(
        Branch,
        on_delete=models.CASCADE,
        related_name="setting",
        verbose_name=_("Branch"),
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
        default="dark",
        verbose_name=_("Screen mode"),
    )
    show_info = models.BooleanField(default=True, verbose_name=_("Show info"))

    def __str__(self):
        return self.branch.name + " - " + self.screen_mode

    class Meta:
        verbose_name = "Branch Settings"
        verbose_name_plural = "Branch Settings"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["branch"]),
        ]


# ======================================
# Branch Infos model
# ======================================
class BranchInfos(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    branch = models.OneToOneField(
        Branch,
        on_delete=models.CASCADE,
        related_name="infos",
        verbose_name=_("Branch"),
    )
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    def __str__(self):
        return self.branch.name + " - " + self.title

    class Meta:
        verbose_name = "Branch Info"
        verbose_name_plural = "Branch Infos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["branch"]),
        ]


class MarketingImage(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="image",
        verbose_name=_("Branch"),
    )
    image = models.ImageField(upload_to="marketing_images/", verbose_name=_("Image"))
    title = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("Title")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    def __str__(self):
        return self.branch.name + " - " + self.title

    class Meta:
        verbose_name = "Marketing Image"
        verbose_name_plural = "Marketing Images"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["branch"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["branch", "title"],
                name="unique_marketing_image_branch_title",
            ),
        ]


# ===================================================
# Video model
# ===================================================
class MarketingVideo(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="video",
        verbose_name=_("Branch"),
    )
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    video = models.FileField(upload_to="videos/", verbose_name=_("Video"))

    def __str__(self):
        return self.branch.name + " - " + self.title

    class Meta:
        verbose_name = "Marketing Video"
        verbose_name_plural = "Marketing Videos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["branch"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["branch", "title"],
                name="unique_marketing_video_branch_title",
            ),
        ]


# ===================================================
#  Service model
# ===================================================
class Service(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="service",
        verbose_name=_("Branch"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    daily_limit = models.IntegerField(default=2000, verbose_name=_("Daily limit"))
    waiting_time = models.IntegerField(
        default=10, verbose_name=_("Wait time (minutes)")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    def __str__(self):
        return self.branch.name + " - " + self.name

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["branch"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["branch", "name"],
                name="unique_service_branch_name",
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
