from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ActivationSignupForm, EmailVerificationForm
from .models import ActivationCode


def _send_verification_email(email: str, verification_code: str) -> None:
    send_mail(
        subject="Your Brainiacs verification code",
        message=(
            "Welcome to Brainiacs!\n\n"
            "Use this verification code to confirm your email and activate sign-in:\n"
            f"{verification_code}\n\n"
            "If you did not request this, you can ignore this email."
        ),
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=[email],
        fail_silently=True,
    )


def _send_activation_alert(username: str, email: str, activation_code: str) -> None:
    send_mail(
        subject="New Activation Signup",
        message=(
            f"Activation code: {activation_code}\n"
            f"Email: {email}\n"
            f"Username: {username}"
        ),
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=[
            getattr(settings, "BRAINIACS_SUPPORT_EMAIL", "hello@brainiacs.academy")
        ],
        fail_silently=True,
    )


def _clear_pending_verification_session(request) -> None:
    request.session.pop("pending_verification_user_id", None)
    request.session.pop("pending_verification_next", None)
    request.session.pop("pending_verification_email", None)

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
                if activation:
                    verification_code = activation.issue_email_verification_code()
                    _send_verification_email(user.email, verification_code)
                _send_activation_alert(
                    form.cleaned_data["username"],
                    form.cleaned_data["email"],
                    form.cleaned_data["activation_code"],
                )
                request.session["pending_verification_user_id"] = user.id
                request.session["pending_verification_next"] = next_url
                request.session["pending_verification_email"] = user.email
                confirm_url = f"{reverse('landing:confirm_email')}?{urlencode({'next': next_url})}"
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

    pending_user_id = request.session.get("pending_verification_user_id")
    user = None
    activation = None
    if pending_user_id:
        User = get_user_model()
        user = User.objects.filter(id=pending_user_id).first()
        if user:
            activation = ActivationCode.objects.filter(user=user).first()

    if not user or not activation:
        _clear_pending_verification_session(request)
        activate_url = f"{reverse('landing:activate')}?{urlencode({'next': next_url})}"
        return redirect(activate_url)

    resent = False
    if request.method == "POST" and request.POST.get("resend") == "1":
        verification_code = activation.issue_email_verification_code()
        _send_verification_email(user.email, verification_code)
        form = EmailVerificationForm()
        resent = True
    elif request.method == "POST":
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            if activation.verify_email_code(form.cleaned_data["verification_code"]):
                _clear_pending_verification_session(request)
                signin_url = f"{reverse('login')}?{urlencode({'next': next_url})}"
                return redirect(signin_url)
            form.add_error("verification_code", "Invalid verification code.")
    else:
        form = EmailVerificationForm()

    return render(
        request,
        "landing/confirm_email.html",
        {
            "form": form,
            "next_url": next_url,
            "email": user.email,
            "resent": resent,
        },
    )
