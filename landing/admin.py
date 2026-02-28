from django.contrib import admin

from .models import ActivationCode, LoginDevice


@admin.register(ActivationCode)
class ActivationCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
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
