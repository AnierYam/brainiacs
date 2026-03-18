from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from brainiacs_site.forms import ActivationCodeSignupForm

from .forms import ActivationSignupForm
from .models import ActivationCode


class ActivationCodeExpiryTests(TestCase):
    def test_activation_signup_form_rejects_expired_code(self):
        ActivationCode.objects.create(
            code="EXPIRED-SIGNUP",
            expires_at=timezone.now() - timedelta(minutes=1),
        )

        form = ActivationSignupForm(
            data={
                "username": "expired-signup-user",
                "email": "expired-signup@example.com",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
                "activation_code": "expired-signup",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["activation_code"],
            ["This activation code has expired."],
        )

    def test_account_signup_form_rejects_expired_code(self):
        ActivationCode.objects.create(
            code="EXPIRED-ACCOUNT",
            expires_at=timezone.now() - timedelta(minutes=1),
        )

        form = ActivationCodeSignupForm(
            data={
                "username": "expired-account-user",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
                "activation_code": "expired-account",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["activation_code"],
            ["This activation code has expired."],
        )

    def test_create_activation_code_command_can_set_24_hour_expiry(self):
        before = timezone.now()

        call_command(
            "create_activation_code",
            "Lina.Akiki2026.,!",
            code_type=ActivationCode.TYPE_TEMPORARY,
            expires_in_hours=24,
        )

        activation_code = ActivationCode.objects.get(code="LINA.AKIKI2026.,!")

        self.assertFalse(activation_code.is_reusable)
        self.assertIsNotNone(activation_code.expires_at)
        self.assertAlmostEqual(
            activation_code.expires_at.timestamp(),
            (before + timedelta(hours=24)).timestamp(),
            delta=5,
        )
