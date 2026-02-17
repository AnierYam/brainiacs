from django.contrib.auth import login
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ActivationSignupForm

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
                login(request, user)
                send_mail(
                    subject='New Activation Signup',
                    message=(
                        f'Activation code: {form.cleaned_data["activation_code"]}\n'
                        f'Email: {form.cleaned_data["email"]}\n'
                        f'Username: {form.cleaned_data["username"]}'
                    ),
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                    recipient_list=[getattr(settings, 'BRAINIACS_SUPPORT_EMAIL', 'hello@brainiacs.academy')],
                    fail_silently=True,
                )
                return redirect(next_url)
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
