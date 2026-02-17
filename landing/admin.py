from django.contrib import admin

from .models import ActivationCode


@admin.register(ActivationCode)
class ActivationCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "activated_email",
        "user",
        "activated_at",
        "linked_at",
        "created_at",
    )
    search_fields = ("code", "activated_email", "user__username")
    list_filter = ("activated_at", "linked_at", "created_at")
    readonly_fields = ("activated_at", "linked_at", "created_at")
