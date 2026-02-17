from urllib.parse import urlencode

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse

from .forms import ActivationRequiredAuthenticationForm


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
