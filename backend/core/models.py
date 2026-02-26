import uuid
from django.db import models
from general_settings.utils import TimeStampedModel
from django.contrib.auth import get_user_model
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, choices=COMPANY_DOMAINS, default="other")
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

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


# ======================================
# branch model
# ======================================
class Branch(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_opened = models.BooleanField(default=True)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    long = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

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


# =============================================
# Payment model
# =============================================
class Payment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD, default="cash"
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


# =======================================
# Branch settings model
# ========================================
class BranchSettings(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    is_voice_enabled = models.BooleanField(default=True)
    voice_style = models.CharField(
        max_length=20, choices=VOICE_STYLE, default="natural"
    )
    allow_remote = models.BooleanField(default=True)
    screen_mode = models.CharField(max_length=20, choices=SCREEN_MODE, default="dark")

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="marketing_images/")
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

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


# ===================================================
# Video model
# ===================================================
class Video(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to="videos/")

    def __str__(self):
        return self.branch.name + " - " + self.title

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["branch"]),
        ]


# ===================================================
#  Service model
# ===================================================
class Service(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    daily_limit = models.IntegerField(default=2000)
    wait_time = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)

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


# ========================================================
# Queue model
# ========================================================
class Queue(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=QUEUE_STATUS, default="waiting")
    queue_number = models.IntegerField(default=1)

    def __str__(self):
        return self.service.name + " - " + self.user.get_full_name()

    class Meta:
        verbose_name = "Queue"
        verbose_name_plural = "Queues"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["service"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(queue_number__gte=1),
                name="queue_number_gte_1",
            ),
        ]
