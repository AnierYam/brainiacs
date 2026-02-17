from django import forms

from .models import ActivationCode, normalize_activation_code


class ActivationStartForm(forms.Form):
    code = forms.CharField(
        label="Activation Code",
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "id": "activate-code",
                "name": "code",
                "placeholder": "Activation Code",
                "required": True,
            }
        ),
    )
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(
            attrs={
                "id": "activate-email",
                "name": "email",
                "placeholder": "Your Email",
                "required": True,
            }
        ),
    )

    activation_code: ActivationCode | None = None

    def clean_code(self) -> str:
        code = normalize_activation_code(self.cleaned_data.get("code"))
        activation_code = ActivationCode.objects.filter(code=code).first()
        if not activation_code:
            raise forms.ValidationError("Invalid activation code.")
        if activation_code.user_id:
            raise forms.ValidationError(
                "This activation code is already linked to an account."
            )
        self.activation_code = activation_code
        return code

    def clean_email(self) -> str:
        return (self.cleaned_data.get("email") or "").strip().lower()

    def clean(self):
        cleaned_data = super().clean()
        activation_code = self.activation_code
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
