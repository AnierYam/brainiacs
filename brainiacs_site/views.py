from urllib.parse import urlencode

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ActivationCodeSignupForm, ActivationRequiredAuthenticationForm


class BrainiacsLoginView(LoginView):
    template_name = "auth/login.html"
    form_class = ActivationRequiredAuthenticationForm
    redirect_authenticated_user = True

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
    activation_code_seed = (
        request.POST.get("activation_code")
        or request.GET.get("activation_code")
        or request.session.get("activation_code", "")
    )

    if request.method == "POST":
        form = ActivationCodeSignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except ValidationError as exc:
                form.add_error("activation_code", exc.messages[0])
            else:
                login(request, user)
                request.session.pop("activation_code", None)
                request.session.pop("activation_email", None)
                return redirect(next_url)
    else:
        form = ActivationCodeSignupForm(
            initial={"activation_code": activation_code_seed}
        )

    signin_url = f"{reverse('login')}?{urlencode({'next': next_url})}"
    activation_url = f"{reverse('landing:activate')}?{urlencode({'next': next_url})}"
    return render(
        request,
        "auth/signup.html",
        {
            "form": form,
            "next_url": next_url,
            "signin_url": signin_url,
            "activation_url": activation_url,
        },
    )
