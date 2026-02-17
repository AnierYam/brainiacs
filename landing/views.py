from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import urlencode

from .forms import ActivationStartForm

def home(request):
    return render(request, 'landing/home.html')


def demo(request):
    return render(request, 'landing/demo.html')


def buy(request):
    return render(request, 'landing/buy.html')


def activate(request):
    next_url = (
        request.GET.get("next")
        or request.POST.get("next")
        or reverse("lessons:missions_home")
    )
    if request.method == 'POST':
        form = ActivationStartForm(request.POST)
        if form.is_valid():
            activation_code = form.activation_code
            email = form.cleaned_data["email"]
            if activation_code:
                activation_code.mark_activated(email)
            request.session["activation_code"] = form.cleaned_data["code"]
            request.session["activation_email"] = email
            send_mail(
                subject='New Activation Request',
                message=(
                    f'Activation code: {form.cleaned_data["code"]}\n'
                    f'Email: {email}'
                ),
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                recipient_list=[getattr(settings, 'BRAINIACS_SUPPORT_EMAIL', 'hello@brainiacs.academy')],
                fail_silently=True,
            )
            signup_url = f"{reverse('signup')}?{urlencode({'next': next_url})}"
            return redirect(signup_url)
    else:
        form = ActivationStartForm(
            initial={
                "code": request.session.get("activation_code", ""),
                "email": request.session.get("activation_email", ""),
            }
        )
    return render(request, "landing/activate.html", {"form": form, "next_url": next_url})
