from urllib.parse import quote

from django.conf import settings
from django.shortcuts import redirect
from django.utils import translation

from landing.site_language import get_site_language


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


class SiteLanguageMiddleware:
    """Apply the site language from the language switch cookie."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        site_lang = get_site_language(request)
        request.site_lang = site_lang
        translation.activate(site_lang)
        request.LANGUAGE_CODE = translation.get_language()
        response = self.get_response(request)
        response.headers["Content-Language"] = request.LANGUAGE_CODE
        translation.deactivate()
        return response
