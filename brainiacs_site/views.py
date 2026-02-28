from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ActivationRequiredAuthenticationForm
from landing.models import ActivationCode
from landing.services import email_service

ONE_TIME_ACTIVATION_CODE = "OTP001"


class BrainiacsLoginView(LoginView):
    template_name = "auth/login.html"
    form_class = ActivationRequiredAuthenticationForm
    redirect_authenticated_user = True

    def _next_url(self) -> str:
        return (
            self.request.GET.get(self.redirect_field_name)
            or self.request.POST.get(self.redirect_field_name)
            or reverse("lessons:missions_home")
        )

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        if getattr(form, "requires_verification", False):
            user = getattr(form, "user_for_verification", None)
            if user:
                next_url = self._next_url()
                confirm_token = email_service.build_confirm_token(user.id)
                self.request.session["pending_verification_user_id"] = user.id
                self.request.session["pending_verification_next"] = next_url
                self.request.session["pending_verification_email"] = user.email
                self.request.session["pending_verification_token"] = confirm_token

                email_sent = email_service.send_verification_email(
                    user,
                    request=self.request,
                    reason="login_resend",
                    next_url=next_url,
                )
                self.request.session["pending_verification_delivery_failed"] = (
                    not email_sent
                )
                if email_sent:
                    messages.info(
                        self.request,
                        "We sent a new verification code to your email.",
                    )
                else:
                    messages.warning(
                        self.request,
                        "Could not send verification email. Please retry in a moment.",
                    )
                confirm_url = (
                    f"{reverse('landing:confirm_email')}?"
                    f"{urlencode({'next': next_url, 'token': confirm_token})}"
                )
                return redirect(confirm_url)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self._next_url()
        context["next_url"] = next_url
        context["local_auth_bypass"] = settings.DEBUG
        context["signup_url"] = f"{reverse('signup')}?{urlencode({'next': next_url})}"
        context["activate_url"] = (
            f"{reverse('landing:activate')}?{urlencode({'next': next_url})}"
        )
        return context


class BrainiacsLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        one_time_activation = None
        if request.user.is_authenticated:
            one_time_activation = ActivationCode.objects.filter(
                user=request.user,
                code=ONE_TIME_ACTIVATION_CODE,
            ).first()

        response = super().post(request, *args, **kwargs)

        if one_time_activation:
            one_time_activation.delete()

        return response


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
    if settings.DEBUG:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect(next_url)
        else:
            form = UserCreationForm()
        form.fields["username"].widget.attrs.update({"placeholder": "Username"})
        form.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        form.fields["password2"].widget.attrs.update({"placeholder": "Confirm Password"})
        return render(
            request,
            "auth/signup_local.html",
            {
                "form": form,
                "next_url": next_url,
                "signin_url": f"{reverse('login')}?{urlencode({'next': next_url})}",
            },
        )

    params = {"next": next_url}
    activation_code = request.GET.get("activation_code") or request.POST.get(
        "activation_code"
    )
    email = request.GET.get("email") or request.POST.get("email")
    if activation_code:
        params["activation_code"] = activation_code
    if email:
        params["email"] = email
    activate_url = f"{reverse('landing:activate')}?{urlencode(params)}"
    return redirect(activate_url)
