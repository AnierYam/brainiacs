from django.conf import settings
from django.db import models
from django.utils import timezone
import secrets


def normalize_activation_code(raw_value: str) -> str:
    return (raw_value or "").strip().upper()


class ActivationCode(models.Model):
    TYPE_TEMPORARY = "temporary"
    TYPE_PERMANENT = "permanent"
    TYPE_CHOICES = (
        (TYPE_TEMPORARY, "Temporary"),
        (TYPE_PERMANENT, "Permanent"),
    )

    code = models.CharField(max_length=64, unique=True, db_index=True)
    is_reusable = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    activated_email = models.EmailField(blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    email_verification_code = models.CharField(max_length=12, blank=True)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="activation_code_link",
    )
    linked_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:
        return self.code

    @property
    def code_type(self) -> str:
        return self.TYPE_PERMANENT if self.is_reusable else self.TYPE_TEMPORARY

    def get_code_type_label(self) -> str:
        return dict(self.TYPE_CHOICES)[self.code_type]

    def set_code_type(self, code_type: str) -> None:
        self.is_reusable = code_type == self.TYPE_PERMANENT

    def is_expired(self, at=None) -> bool:
        if self.expires_at is None:
            return False
        reference_time = at or timezone.now()
        return self.expires_at <= reference_time

    def save(self, *args, **kwargs):
        self.code = normalize_activation_code(self.code)
        if self.activated_email:
            self.activated_email = self.activated_email.strip().lower()
        super().save(*args, **kwargs)

    def mark_activated(self, email: str) -> None:
        email_value = (email or "").strip().lower()
        updated_fields = []
        if email_value and self.activated_email != email_value:
            self.activated_email = email_value
            updated_fields.append("activated_email")
        if self.activated_at is None:
            self.activated_at = timezone.now()
            updated_fields.append("activated_at")
        if updated_fields:
            self.save(update_fields=updated_fields)

    @classmethod
    def generate_linked_code(cls, base_code: str) -> str:
        normalized_base = normalize_activation_code(base_code)
        suffix_length = 16
        reserved_length = suffix_length + 1
        prefix = normalized_base[: max(0, 64 - reserved_length)]
        while True:
            suffix = secrets.token_hex(suffix_length // 2).upper()
            candidate = f"{prefix}-{suffix}" if prefix else suffix
            if not cls.objects.filter(code=candidate).exists():
                return candidate

    def create_user_link(self, user, email: str = ""):
        timestamp = timezone.now()
        linked_activation = self.__class__(
            code=self.generate_linked_code(self.code),
            activated_email=(email or "").strip().lower(),
            activated_at=timestamp,
            user=user,
            linked_at=timestamp,
        )
        linked_activation.save()
        return linked_activation

    def issue_email_verification_code(self) -> str:
        verification_code = f"{secrets.randbelow(1_000_000):06d}"
        self.email_verification_code = verification_code
        self.email_verification_sent_at = timezone.now()
        self.email_verified_at = None
        self.save(
            update_fields=[
                "email_verification_code",
                "email_verification_sent_at",
                "email_verified_at",
            ]
        )
        return verification_code

    def verify_email_code(self, code_input: str) -> bool:
        expected = (self.email_verification_code or "").strip()
        candidate = (code_input or "").strip()
        if not expected or candidate != expected:
            return False
        self.email_verified_at = timezone.now()
        self.email_verification_code = ""
        self.save(update_fields=["email_verified_at", "email_verification_code"])
        return True


class LoginDevice(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="login_devices",
    )
    device_hash = models.CharField(max_length=64, db_index=True)
    first_seen_at = models.DateTimeField(default=timezone.now)
    last_seen_at = models.DateTimeField(default=timezone.now)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    last_user_agent = models.TextField(blank=True)
    last_alert_sent_at = models.DateTimeField(null=True, blank=True)
    known_ips = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-last_seen_at"]
        unique_together = ("user", "device_hash")
        indexes = [
            models.Index(fields=["user", "device_hash"]),
            models.Index(fields=["last_seen_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.user_id}:{self.device_hash[:12]}"
