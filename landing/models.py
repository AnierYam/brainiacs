from django.conf import settings
from django.db import models
from django.utils import timezone
import secrets


def normalize_activation_code(raw_value: str) -> str:
    return (raw_value or "").strip().upper()


class ActivationCode(models.Model):
    code = models.CharField(max_length=64, unique=True, db_index=True)
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
