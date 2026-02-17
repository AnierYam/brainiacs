from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

def home(request):
    return render(request, 'landing/home.html')


def demo(request):
    return render(request, 'landing/demo.html')


def buy(request):
    return render(request, 'landing/buy.html')


def activate(request):
    if request.method == 'POST':
        code = (request.POST.get('code') or '').strip()
        email = (request.POST.get('email') or '').strip()
        success = bool(code and email)
        if success:
            send_mail(
                subject='New Activation Request',
                message=f'Activation code: {code}\nEmail: {email}',
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                recipient_list=[getattr(settings, 'BRAINIACS_SUPPORT_EMAIL', 'hello@brainiacs.academy')],
                fail_silently=True,
            )
        return render(request, 'landing/activate.html', {'success': success})
    return render(request, 'landing/activate.html')
