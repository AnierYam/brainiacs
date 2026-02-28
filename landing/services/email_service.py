import logging
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from ..models import ActivationCode

logger = logging.getLogger("brainiacs.email")
CONFIRM_EMAIL_SIGNING_SALT = "landing.confirm_email"


def build_confirm_token(user_id: int) -> str:
    return signing.dumps({"user_id": user_id}, salt=CONFIRM_EMAIL_SIGNING_SALT)


def resolve_pending_user_from_token(token: str | None):
    if not token:
        return None
    max_age_seconds = int(
        getattr(settings, "BRAINIACS_EMAIL_CONFIRM_TOKEN_MAX_AGE", 60 * 60 * 24)
    )
    try:
        payload = signing.loads(
            token,
            salt=CONFIRM_EMAIL_SIGNING_SALT,
            max_age=max_age_seconds,
        )
    except signing.BadSignature:
        return None
    user_id = payload.get("user_id")
    if not user_id:
        return None
    User = get_user_model()
    return User.objects.filter(id=user_id).first()


def _absolute_url(path: str, request=None) -> str:
    if request is not None:
        return request.build_absolute_uri(path)
    base = getattr(settings, "SITE_URL", "http://127.0.0.1:8000").rstrip("/")
    return f"{base}{path}"


def _confirm_url(user, request=None, next_url: str | None = None) -> str:
    token = build_confirm_token(user.id)
    destination = next_url or reverse("lessons:missions_home")
    query = urlencode({"next": destination, "token": token})
    path = f"{reverse('landing:confirm_email')}?{query}"
    return _absolute_url(path, request=request)


def _logo_url(request=None) -> str:
    return _absolute_url("/static/icons/brainiacs_logo.png", request=request)


def _render_bodies(
    template_name: str,
    context: dict,
    request=None,
) -> tuple[str, str]:
    render_context = {"logo_url": _logo_url(request=request), **context}
    text_body = render_to_string(f"emails/{template_name}.txt", render_context).strip()
    html_body = render_to_string(f"emails/{template_name}.html", render_context)
    return text_body, html_body


def _send_message(message: EmailMultiAlternatives, *, user, reason: str) -> bool:
    try:
        sent_count = message.send(fail_silently=False)
    except Exception:
        logger.exception(
            "Email send failed (reason=%s, user_id=%s, email=%s)",
            reason,
            getattr(user, "id", None),
            getattr(user, "email", ""),
        )
        return False
    if sent_count != 1:
        logger.error(
            "Email send returned unexpected count=%s (reason=%s, user_id=%s, email=%s)",
            sent_count,
            reason,
            getattr(user, "id", None),
            getattr(user, "email", ""),
        )
        return False
    logger.info(
        "Email sent (reason=%s, user_id=%s, email=%s)",
        reason,
        getattr(user, "id", None),
        getattr(user, "email", ""),
    )
    return True


def send_verification_email(user, request=None, reason: str = "signup", next_url=None) -> bool:
    recipient = (getattr(user, "email", "") or "").strip().lower()
    if not recipient:
        logger.error(
            "Verification email skipped: user has no email (reason=%s, user_id=%s)",
            reason,
            getattr(user, "id", None),
        )
        return False
    activation = ActivationCode.objects.filter(user=user).first()
    if not activation:
        logger.error(
            "Verification email skipped: no activation linked (reason=%s, user_id=%s, email=%s)",
            reason,
            getattr(user, "id", None),
            recipient,
        )
        return False

    verification_code = activation.issue_email_verification_code()
    confirm_url = _confirm_url(user, request=request, next_url=next_url)
    subject = "Your Brainiacs verification code"
    context = {
        "subject": subject,
        "username": user.get_username(),
        "verification_code": verification_code,
        "confirm_url": confirm_url,
        "cta_url": confirm_url,
        "cta_label": "Confirm email",
        "reason": reason,
    }
    text_body, html_body = _render_bodies("verification", context, request=request)
    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=getattr(settings, "BRAINIACS_OUTBOUND_FROM_EMAIL", None),
        to=[recipient],
    )
    message.attach_alternative(html_body, "text/html")
    return _send_message(message, user=user, reason=reason)


def send_kit_activation_email(user, kit, request=None) -> bool:
    recipient = (getattr(user, "email", "") or "").strip().lower()
    if not recipient:
        logger.error(
            "Kit activation email skipped: user has no email (user_id=%s)",
            getattr(user, "id", None),
        )
        return False
    kit_code = getattr(kit, "code", "") or "your Brainiacs kit"
    next_steps_url = _absolute_url(reverse("lessons:missions_home"), request=request)
    subject = "Your Brainiacs kit is activated"
    context = {
        "subject": subject,
        "username": user.get_username(),
        "kit_code": kit_code,
        "next_steps_url": next_steps_url,
        "cta_url": next_steps_url,
        "cta_label": "Go to lessons",
    }
    text_body, html_body = _render_bodies("kit_activated", context, request=request)
    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=getattr(settings, "BRAINIACS_OUTBOUND_FROM_EMAIL", None),
        to=[recipient],
    )
    message.attach_alternative(html_body, "text/html")
    return _send_message(message, user=user, reason="kit_activation")


def send_login_alert_email(
    user,
    ip_address: str = "unknown",
    device_summary: str = "",
) -> bool:
    recipient = (getattr(user, "email", "") or "").strip().lower()
    if not recipient:
        logger.info(
            "Login alert skipped: user has no email (user_id=%s)",
            getattr(user, "id", None),
        )
        return False
    timestamp = timezone.localtime().strftime("%Y-%m-%d %H:%M %Z")
    subject = "Brainiacs sign-in alert"
    context = {
        "subject": subject,
        "username": user.get_username(),
        "timestamp": timestamp,
        "ip_address": ip_address,
        "device_summary": device_summary,
        "cta_url": "",
        "cta_label": "",
    }
    text_body, html_body = _render_bodies("login_alert", context)
    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=getattr(settings, "BRAINIACS_OUTBOUND_FROM_EMAIL", None),
        to=[recipient],
    )
    message.attach_alternative(html_body, "text/html")
    return _send_message(message, user=user, reason="login_alert")


def _mask_activation_code(raw_code: str) -> str:
    code = (raw_code or "").strip()
    if not code:
        return ""
    if len(code) <= 4:
        return "*" * len(code)
    if len(code) <= 8:
        return f"{code[:2]}...{code[-2:]}"
    return f"{code[:4]}...{code[-4:]}"


def send_activation_admin_alert_email(
    username: str, email: str, activation_code: str
) -> bool:
    support_email = getattr(settings, "BRAINIACS_SUPPORT_EMAIL", "").strip()
    if not support_email:
        logger.error("Activation admin alert skipped: BRAINIACS_SUPPORT_EMAIL not set")
        return False
    subject = "New Activation Signup"
    admin_url = _absolute_url("/admin/landing/activationcode/")
    body = render_to_string(
        "emails/admin_activation_alert.txt",
        {
            "username": username,
            "email": email,
            "masked_activation_code": _mask_activation_code(activation_code),
            "admin_url": admin_url,
        },
    ).strip()
    message = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=getattr(settings, "BRAINIACS_OUTBOUND_FROM_EMAIL", None),
        to=[support_email],
    )
    class _AdminUser:
        id = "admin-alert"
        email = support_email

    return _send_message(message, user=_AdminUser(), reason="activation_admin_alert")
