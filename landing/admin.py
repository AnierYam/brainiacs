from django.contrib import admin
from django import forms

from .models import ActivationCode, LoginDevice


class ActivationCodeAdminForm(forms.ModelForm):
    code_type = forms.ChoiceField(
        label="Code type",
        choices=ActivationCode.TYPE_CHOICES,
    )

    class Meta:
        model = ActivationCode
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["code_type"].initial = (
            self.instance.code_type if self.instance and self.instance.pk else ActivationCode.TYPE_TEMPORARY
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_code_type(self.cleaned_data["code_type"])
        if commit:
            instance.save()
            self.save_m2m()
        return instance


@admin.register(ActivationCode)
class ActivationCodeAdmin(admin.ModelAdmin):
    form = ActivationCodeAdminForm
    list_display = (
        "code",
        "code_type_display",
        "expires_at",
        "activated_email",
        "user",
        "activated_at",
        "email_verification_sent_at",
        "email_verified_at",
        "linked_at",
        "created_at",
    )
    search_fields = ("code", "activated_email", "user__username")
    list_filter = (
        "is_reusable",
        "expires_at",
        "activated_at",
        "email_verification_sent_at",
        "email_verified_at",
        "linked_at",
        "created_at",
    )
    fields = (
        "code",
        "code_type",
        "expires_at",
        "activated_email",
        "user",
        "activated_at",
        "email_verification_sent_at",
        "email_verified_at",
        "linked_at",
        "created_at",
    )
    readonly_fields = (
        "activated_at",
        "email_verification_sent_at",
        "email_verified_at",
        "linked_at",
        "created_at",
    )

    @admin.display(description="Type")
    def code_type_display(self, obj):
        return obj.get_code_type_label()


@admin.register(LoginDevice)
class LoginDeviceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "device_hash",
        "last_ip",
        "first_seen_at",
        "last_seen_at",
        "last_alert_sent_at",
    )
    search_fields = ("user__username", "user__email", "device_hash", "last_ip")
    list_filter = ("first_seen_at", "last_seen_at", "last_alert_sent_at")
    readonly_fields = (
        "user",
        "device_hash",
        "first_seen_at",
        "last_seen_at",
        "last_ip",
        "last_user_agent",
        "last_alert_sent_at",
        "known_ips",
    )
