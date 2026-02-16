from urllib.parse import urlencode

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse


class BrainiacsLoginView(LoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = (
            self.request.GET.get(self.redirect_field_name)
            or self.request.POST.get(self.redirect_field_name)
            or reverse("lessons:missions_home")
        )
        context["next_url"] = next_url
        context["signup_url"] = f"{reverse('signup')}?{urlencode({'next': next_url})}"
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

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
    else:
        form = UserCreationForm()

    signin_url = f"{reverse('login')}?{urlencode({'next': next_url})}"
    return render(
        request,
        "auth/signup.html",
        {
            "form": form,
            "next_url": next_url,
            "signin_url": signin_url,
        },
    )
