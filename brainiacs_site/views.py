from urllib.parse import urlencode

from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from .forms import ActivationRequiredAuthenticationForm


class BrainiacsLoginView(LoginView):
    template_name = "auth/login.html"
    form_class = ActivationRequiredAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        if getattr(user, "email", ""):
            timestamp = timezone.localtime().strftime("%Y-%m-%d %H:%M %Z")
            ip_address = self.request.META.get("REMOTE_ADDR", "unknown")
            send_mail(
                subject="Brainiacs sign-in alert",
                message=(
                    f"Hi {user.get_username()},\n\n"
                    "Your Brainiacs account was signed in.\n"
                    f"Time: {timestamp}\n"
                    f"IP address: {ip_address}\n\n"
                    "If this wasn't you, please reset your password."
                ),
                from_email=getattr(settings, "BRAINIACS_OUTBOUND_FROM_EMAIL", None),
                recipient_list=[user.email],
                fail_silently=True,
            )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = (
            self.request.GET.get(self.redirect_field_name)
            or self.request.POST.get(self.redirect_field_name)
            or reverse("lessons:missions_home")
        )
        context["next_url"] = next_url
        context["activate_url"] = (
            f"{reverse('landing:activate')}?{urlencode({'next': next_url})}"
        )
        return context


def home_entry(request):
    if request.user.is_authenticated:
        return redirect("lessons:missions_home")
    return redirect("login")


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("lessons:missions_home")

    next_url = (
        request.GET.get("next")
        or request.POST.get("next")
        or reverse("lessons:missions_home")
    )
    signin_url = f"{reverse('login')}?{urlencode({'next': next_url})}"
    return redirect(signin_url)
