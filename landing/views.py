from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ActivationSignupForm, EmailVerificationForm
from .models import ActivationCode
from .site_language import (
    get_site_copy,
    get_site_language,
    localize_form,
    translate_site_message,
)
from .services import email_service


def _clear_pending_verification_session(request) -> None:
    request.session.pop("pending_verification_user_id", None)
    request.session.pop("pending_verification_next", None)
    request.session.pop("pending_verification_email", None)
    request.session.pop("pending_verification_token", None)
    request.session.pop("pending_verification_delivery_failed", None)


def _site_context(request):
    lang = get_site_language(request)
    return lang, {"site_lang": lang, "copy": get_site_copy(lang)}

def home(request):
    _, context = _site_context(request)
    return render(request, "landing/home.html", context)


def demo(request):
    _, context = _site_context(request)
    return render(request, "landing/demo.html", context)


def buy(request):
    _, context = _site_context(request)
    return render(request, "landing/buy.html", context)


def activate(request):
    lang, context = _site_context(request)
    if request.user.is_authenticated:
        return redirect("lessons:missions_home")

    next_url = (
        request.GET.get("next")
        or request.POST.get("next")
        or reverse("lessons:missions_home")
    )

    if request.method == 'POST':
        form = ActivationSignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except ValidationError as exc:
                form.add_error(
                    "activation_code",
                    translate_site_message(exc.messages[0], lang),
                )
            else:
                activation = ActivationCode.objects.filter(user=user).first()
                email_sent = email_service.send_verification_email(
                    user,
                    request=request,
                    reason="signup",
                    next_url=next_url,
                )
                if activation:
                    email_service.send_kit_activation_email(
                        user=user,
                        kit=activation,
                        request=request,
                    )
                email_service.send_activation_admin_alert_email(
                    form.cleaned_data["username"],
                    form.cleaned_data["email"],
                    form.cleaned_data["activation_code"],
                )
                confirm_token = email_service.build_confirm_token(user.id)
                request.session["pending_verification_user_id"] = user.id
                request.session["pending_verification_next"] = next_url
                request.session["pending_verification_email"] = user.email
                request.session["pending_verification_token"] = confirm_token
                request.session["pending_verification_delivery_failed"] = not email_sent
                confirm_url = (
                    f"{reverse('landing:confirm_email')}?"
                    f"{urlencode({'next': next_url, 'token': confirm_token})}"
                )
                return redirect(confirm_url)
    else:
        form = ActivationSignupForm(
            initial={
                "activation_code": request.GET.get("activation_code")
                or request.session.get("activation_code", ""),
                "email": request.GET.get("email")
                or request.session.get("activation_email", ""),
            }
        )
    localize_form(form, lang, "activate_signup")
    context.update({"form": form, "next_url": next_url})
    return render(request, "landing/activate.html", context)


def confirm_email(request):
    lang, context = _site_context(request)
    if request.user.is_authenticated:
        return redirect("lessons:missions_home")

    next_url = (
        request.GET.get("next")
        or request.POST.get("next")
        or request.session.get("pending_verification_next")
        or reverse("lessons:missions_home")
    )
    token = (
        request.GET.get("token")
        or request.POST.get("token")
        or request.session.get("pending_verification_token")
    )

    pending_user_id = request.session.get("pending_verification_user_id")
    user = None
    activation = None
    if pending_user_id:
        User = get_user_model()
        user = User.objects.filter(id=pending_user_id).first()
    if user is None:
        user = email_service.resolve_pending_user_from_token(token)
    if user:
        activation = ActivationCode.objects.filter(user=user).first()

    if not user or not activation:
        _clear_pending_verification_session(request)
        activate_url = f"{reverse('landing:activate')}?{urlencode({'next': next_url})}"
        return redirect(activate_url)

    request.session["pending_verification_user_id"] = user.id
    request.session["pending_verification_next"] = next_url
    request.session["pending_verification_email"] = user.email
    if token:
        request.session["pending_verification_token"] = token

    resent = False
    delivery_warning = bool(request.session.get("pending_verification_delivery_failed"))
    if request.method == "POST" and request.POST.get("resend") == "1":
        email_sent = email_service.send_verification_email(
            user,
            request=request,
            reason="confirm_resend",
            next_url=next_url,
        )
        form = EmailVerificationForm()
        resent = True
        delivery_warning = not email_sent
        request.session["pending_verification_delivery_failed"] = delivery_warning
    elif request.method == "POST":
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            if activation.verify_email_code(form.cleaned_data["verification_code"]):
                _clear_pending_verification_session(request)
                signin_url = f"{reverse('login')}?{urlencode({'next': next_url})}"
                return redirect(signin_url)
            form.add_error(
                "verification_code",
                translate_site_message("Invalid verification code.", lang),
            )
        delivery_warning = bool(request.session.get("pending_verification_delivery_failed"))
    else:
        form = EmailVerificationForm()
    localize_form(form, lang, "verify_email")

    context.update(
        {
            "form": form,
            "next_url": next_url,
            "token": token,
            "email": user.email,
            "resent": resent,
            "delivery_warning": delivery_warning,
        }
    )
    return render(request, "landing/confirm_email.html", context)
