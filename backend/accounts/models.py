import uuid
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin,
    AbstractUser,
)
from django.utils import timezone
from general_settings.constants import OTP_EXPIRATION_TIME
from general_settings.utils import TimeStampedModel
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("Users must have an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, PermissionsMixin):
    """
    Custom user model that extends AbstractBaseUser and PermissionsMixin.
    Uses phone_number as the unique identifier instead of username.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country_code = models.CharField(
        max_length=5,
        default="226",
        verbose_name=_("Code pays"),
        help_text=_("Code pays de l'utilisateur"),
    )
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Numéro de téléphone"),
        help_text=_("Numéro de téléphone unique de l'utilisateur"),
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name=_("Email"),
        help_text=_("Email address"),
    )
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} - {self.email}"
        return self.email

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name or self.email

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        indexes = [
            models.Index(fields=["phone_number"]),
            models.Index(fields=["email"]),
            models.Index(fields=["country_code"]),
            models.Index(fields=["is_active"]),
        ]


class OTP(TimeStampedModel):
    """
    Model for phone OTP (One-Time Password) verification.
    Includes security features like expiration, attempt limits, and account locking.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="otp",
        verbose_name=_("Utilisateur"),
    )
    code = models.TextField(
        verbose_name=_("Code OTP"),
        db_index=True,
        help_text=_("Code OTP envoyé au numéro de téléphone"),
    )
    max_attempts = models.IntegerField(
        default=0,
        verbose_name=_("Tentatives"),
        help_text=_("Nombre de tentatives de vérification"),
    )
    locked_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Verrouillé jusqu'à"),
        help_text=_("Date jusqu'à laquelle le compte est verrouillé"),
    )
    used_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Utilisé le"))
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("OTP vérifié"),
        db_index=True,
        help_text=_("Indique si l'OTP a été vérifié"),
    )

    def is_expired(self):
        """Check if OTP has expired."""
        return (
            self.updated_at + timezone.timedelta(minutes=OTP_EXPIRATION_TIME)
            < timezone.now()
        )

    def is_locked(self):
        """Check if OTP attempts are locked."""
        if self.locked_until and self.locked_until > timezone.now():
            return True
        return False

    def __str__(self):
        return f"{self.user.phone_number} - OTP: {'*' * 4}{self.code[-2:]}"

    class Meta:
        verbose_name = _("OTP")
        verbose_name_plural = _("OTPs")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_verified"]),
            models.Index(fields=["created_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(max_attempts__gte=0), name="max_attempts_non_negative"
            ),
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(is_verified=False),
                name="one_active_otp_per_user",
            ),
        ]


class UserSettings(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user_settings",
        verbose_name=_("Utilisateur"),
    )
    sms_notifications = models.BooleanField(
        default=True,
        verbose_name=_("Notifications SMS"),
        help_text=_("Activate SMS notifications"),
    )
    email_notifications = models.BooleanField(
        default=True,
        verbose_name=_("Notifications Email"),
        help_text=_("Activate email notifications"),
    )
    reminder_minutes = models.IntegerField(
        default=15,
        verbose_name=_("Minutes before reminder"),
        help_text=_("Minutes before reminder"),
    )

    class Meta:
        verbose_name = _("User settings")
        verbose_name_plural = _("User settings")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.email}"
