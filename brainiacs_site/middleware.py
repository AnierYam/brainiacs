from urllib.parse import quote

from django.conf import settings
from django.shortcuts import redirect


class LessonsLoginRequiredMiddleware:
    """Require authentication before accessing lessons routes."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/lessons/") and not request.user.is_authenticated:
            login_url = settings.LOGIN_URL
            next_path = quote(request.get_full_path())
            return redirect(f"{login_url}?next={next_path}")
        return self.get_response(request)
