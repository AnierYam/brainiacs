from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import ActivationCode, normalize_activation_code


class ActivationSignupForm(UserCreationForm):
    activation_code = forms.CharField(
        label="Activation Code",
        max_length=64,
    )
    email = forms.EmailField(label="Your Email")

    class Meta(UserCreationForm.Meta):
        fields = ("username", "activation_code", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._activation_code_obj: ActivationCode | None = None
        self.fields["username"].widget.attrs.update(
            {
                "id": "activate-username",
                "placeholder": "Username",
                "required": True,
            }
        )
        self.fields["activation_code"].widget.attrs.update(
            {
                "id": "activate-code",
                "placeholder": "Activation Code",
                "required": True,
                "autocapitalize": "characters",
                "autocomplete": "off",
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "id": "activate-email",
                "placeholder": "Your Email",
                "required": True,
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "id": "activate-password1",
                "placeholder": "Password",
                "required": True,
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "id": "activate-password2",
                "placeholder": "Confirm Password",
                "required": True,
            }
        )

    def clean_activation_code(self) -> str:
        code = normalize_activation_code(self.cleaned_data.get("activation_code"))
        activation_code = ActivationCode.objects.filter(code=code).first()
        if not activation_code:
            raise forms.ValidationError("Invalid activation code.")
        if activation_code.user_id:
            raise forms.ValidationError(
                "This activation code is already linked to an account."
            )
        self._activation_code_obj = activation_code
        return code

    def clean_email(self) -> str:
        return (self.cleaned_data.get("email") or "").strip().lower()

    def clean(self):
        cleaned_data = super().clean()
        activation_code = self._activation_code_obj
        email = cleaned_data.get("email")
        if (
            activation_code
            and email
            and activation_code.activated_email
            and activation_code.activated_email != email
        ):
            self.add_error(
                "email",
                "This code was already activated with a different email.",
            )
        return cleaned_data

    def save(self, commit=True):
        if not commit:
            raise ValueError("ActivationSignupForm.save() requires commit=True.")
        if not self._activation_code_obj:
            raise ValidationError("Activation code validation did not run.")

        activation_code_id = self._activation_code_obj.id
        user = super().save(commit=False)
        email = self.cleaned_data["email"]

        with transaction.atomic():
            activation_code = ActivationCode.objects.select_for_update().get(
                id=activation_code_id
            )
            if activation_code.user_id:
                raise ValidationError(
                    "This activation code has already been used. Try another code."
                )

            if hasattr(user, "email"):
                user.email = email
            user.save()

            activation_code.user = user
            activation_code.activated_email = email
            activation_code.linked_at = timezone.now()
            if activation_code.activated_at is None:
                activation_code.activated_at = timezone.now()
            activation_code.save(
                update_fields=[
                    "user",
                    "activated_email",
                    "linked_at",
                    "activated_at",
                ]
            )
        return user
