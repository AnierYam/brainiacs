from django.conf import settings
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from landing.models import ActivationCode, normalize_activation_code


class ActivationRequiredAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requires_verification = False
        self.user_for_verification = None

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if settings.DEBUG:
            return
        if user.is_staff or user.is_superuser:
            return
        activation = ActivationCode.objects.filter(user=user).first()
        if not activation:
            raise ValidationError(
                "This account is not linked to an activation code. "
                "Activate your kit before signing in.",
                code="activation_required",
            )
        if activation.email_verified_at is None:
            # Backward compatibility: accounts linked before email verification
            # rollout had no verification challenge issued.
            if (
                activation.email_verification_sent_at is None
                and not (activation.email_verification_code or "").strip()
            ):
                activation.email_verified_at = timezone.now()
                activation.save(update_fields=["email_verified_at"])
                return
            self.requires_verification = True
            self.user_for_verification = user
            raise ValidationError(
                "You must confirm your email before signing in. "
                "Check your inbox for the verification code.",
                code="email_verification_required",
            )


class ActivationCodeSignupForm(UserCreationForm):
    activation_code = forms.CharField(
        label="Activation code",
        max_length=64,
        strip=True,
        help_text="Enter the code supplied with your kit.",
    )

    class Meta(UserCreationForm.Meta):
        fields = ("username", "activation_code")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._activation_code_obj: ActivationCode | None = None
        self.fields["activation_code"].widget.attrs.update(
            {
                "autocomplete": "off",
                "autocapitalize": "characters",
                "placeholder": "Activation Code",
            }
        )

    def clean_activation_code(self) -> str:
        code_value = normalize_activation_code(self.cleaned_data.get("activation_code"))
        if not code_value:
            raise forms.ValidationError("Activation code is required.")
        activation_code = ActivationCode.objects.filter(code=code_value).first()
        if not activation_code:
            raise forms.ValidationError("Invalid activation code.")
        if activation_code.user_id and not activation_code.is_reusable:
            raise forms.ValidationError(
                "This activation code is already linked to another account."
            )
        self._activation_code_obj = activation_code
        return code_value

    def save(self, commit=True):
        if not commit:
            raise ValueError("ActivationCodeSignupForm.save() requires commit=True.")

        if not self._activation_code_obj:
            raise ValidationError("Activation code validation did not run.")

        activation_code_id = self._activation_code_obj.id
        user = super().save(commit=False)

        with transaction.atomic():
            activation_code = ActivationCode.objects.select_for_update().get(
                id=activation_code_id
            )
            if activation_code.user_id and not activation_code.is_reusable:
                raise ValidationError(
                    "This activation code has already been used. Try another code."
                )

            if hasattr(user, "email") and activation_code.activated_email:
                user.email = activation_code.activated_email
            user.save()

            if activation_code.is_reusable:
                activation_code.create_user_link(
                    user=user,
                    email=getattr(user, "email", "") or "",
                )
            else:
                activation_code.user = user
                activation_code.linked_at = timezone.now()
                if activation_code.activated_at is None:
                    activation_code.activated_at = timezone.now()
                activation_code.save(update_fields=["user", "linked_at", "activated_at"])

        return user
