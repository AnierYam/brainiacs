from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.db import transaction
from django.dispatch import receiver
from django.utils import timezone

from landing.models import LoginDevice
from landing.services import email_service
from landing.services.security import build_device_hash, get_client_ip, summarize_user_agent


@receiver(user_logged_in)
def track_user_login(sender, request, user, **kwargs):
    if request is None or not getattr(user, "is_authenticated", False):
        return

    user_email = (getattr(user, "email", "") or "").strip()
    if not user_email:
        return

    now = timezone.now()
    device_hash = build_device_hash(request)
    client_ip = get_client_ip(request)
    raw_user_agent = (request.META.get("HTTP_USER_AGENT", "") or "").strip()
    user_agent = raw_user_agent[:1024]
    cooldown_seconds = int(
        getattr(settings, "BRAINIACS_LOGIN_ALERT_COOLDOWN_SECONDS", 60 * 60 * 12)
    )

    with transaction.atomic():
        device, created = LoginDevice.objects.select_for_update().get_or_create(
            user=user,
            device_hash=device_hash,
            defaults={
                "first_seen_at": now,
                "last_seen_at": now,
                "last_ip": client_ip or None,
                "last_user_agent": user_agent,
                "known_ips": [client_ip] if client_ip else [],
            },
        )

        known_ips = list(device.known_ips or [])
        ip_is_new = bool(client_ip) and (client_ip not in known_ips)
        if ip_is_new:
            known_ips.append(client_ip)

        should_alert = created or ip_is_new
        if should_alert and device.last_alert_sent_at:
            elapsed_seconds = (now - device.last_alert_sent_at).total_seconds()
            if elapsed_seconds < cooldown_seconds:
                should_alert = False

        device.last_seen_at = now
        if client_ip:
            device.last_ip = client_ip
        device.last_user_agent = user_agent
        device.known_ips = known_ips
        if should_alert:
            device.last_alert_sent_at = now
        device.save(
            update_fields=[
                "last_seen_at",
                "last_ip",
                "last_user_agent",
                "known_ips",
                "last_alert_sent_at",
            ]
        )

    if should_alert:
        email_service.send_login_alert_email(
            user,
            ip_address=client_ip or "unknown",
            device_summary=summarize_user_agent(user_agent) or "unknown device",
        )

