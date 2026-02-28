import os
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from landing.models import ActivationCode
from landing.services import email_service


class Command(BaseCommand):
    help = "Send a specific Brainiacs email type for manual verification."

    def add_arguments(self, parser):
        parser.add_argument(
            "--to",
            dest="to_email",
            help="Recipient email address. Falls back to TEST_EMAIL_TO or BRAINIACS_SUPPORT_EMAIL.",
        )
        parser.add_argument(
            "--type",
            dest="email_type",
            choices=["verification", "login", "kit", "admin"],
            default="verification",
            help="Type of email to send.",
        )

    def _get_or_create_test_user(self, recipient: str):
        User = get_user_model()
        user, _ = User.objects.get_or_create(
            username="email-test-user",
            defaults={"email": recipient},
        )
        if getattr(user, "email", "") != recipient:
            user.email = recipient
            user.save(update_fields=["email"])
        return user

    def _get_or_create_activation(self, user, recipient: str):
        activation = ActivationCode.objects.filter(user=user).first()
        if activation:
            return activation
        candidate = f"EMAILTEST-{uuid.uuid4().hex[:8].upper()}"
        activation = ActivationCode.objects.create(
            code=candidate,
            user=user,
            activated_email=recipient,
            linked_at=timezone.now(),
            activated_at=timezone.now(),
        )
        return activation

    def handle(self, *args, **options):
        recipient = (
            options.get("to_email")
            or os.getenv("TEST_EMAIL_TO")
            or getattr(settings, "BRAINIACS_SUPPORT_EMAIL", "")
        )
        if not recipient:
            raise CommandError(
                "No recipient provided. Pass --to or set TEST_EMAIL_TO / BRAINIACS_SUPPORT_EMAIL."
            )

        email_type = options.get("email_type")
        user = self._get_or_create_test_user(recipient)
        activation = self._get_or_create_activation(user, recipient)

        if email_type == "verification":
            sent = email_service.send_verification_email(
                user,
                reason="test_command",
            )
        elif email_type == "login":
            sent = email_service.send_login_alert_email(
                user,
                ip_address="203.0.113.24",
                device_summary="test-email-command",
            )
        elif email_type == "kit":
            sent = email_service.send_kit_activation_email(user=user, kit=activation)
        else:
            sent = email_service.send_activation_admin_alert_email(
                username=user.get_username(),
                email=recipient,
                activation_code=activation.code,
            )

        if not sent:
            raise CommandError(
                f"Email send reported failure for type '{email_type}' to {recipient}."
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"Sent '{email_type}' email successfully to {recipient}."
            )
        )

