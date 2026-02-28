from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ActivationSignupForm, EmailVerificationForm
from .models import ActivationCode
from .services import email_service


def _clear_pending_verification_session(request) -> None:
    request.session.pop("pending_verification_user_id", None)
    request.session.pop("pending_verification_next", None)
    request.session.pop("pending_verification_email", None)
    request.session.pop("pending_verification_token", None)
    request.session.pop("pending_verification_delivery_failed", None)

def home(request):
    return render(request, 'landing/home.html')


def demo(request):
    return render(request, 'landing/demo.html')


def buy(request):
    return render(request, 'landing/buy.html')


def activate(request):
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
                form.add_error("activation_code", exc.messages[0])
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
    return render(request, "landing/activate.html", {"form": form, "next_url": next_url})


def confirm_email(request):
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
            form.add_error("verification_code", "Invalid verification code.")
        delivery_warning = bool(request.session.get("pending_verification_delivery_failed"))
    else:
        form = EmailVerificationForm()

    return render(
        request,
        "landing/confirm_email.html",
        {
            "form": form,
            "next_url": next_url,
            "token": token,
            "email": user.email,
            "resent": resent,
            "delivery_warning": delivery_warning,
        },
    )
