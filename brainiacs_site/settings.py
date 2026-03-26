import os
from pathlib import Path
import importlib.util
from django.core.exceptions import ImproperlyConfigured

try:
    import dj_database_url
except ImportError:  # pragma: no cover - optional during local bootstrap
    dj_database_url = None


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_list(name: str, default: str = "") -> list[str]:
    raw_value = os.getenv(name, default)
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def _env_first(names: tuple[str, ...], default: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value not in (None, ""):
            return value
    return default


def _env_bool_first(names: tuple[str, ...], default: bool) -> bool:
    for name in names:
        if os.getenv(name) is not None:
            return _env_bool(name, default)
    return default


def _env_int_first(names: tuple[str, ...], default: int) -> int:
    for name in names:
        value = os.getenv(name)
        if value not in (None, ""):
            return int(value)
    return default

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
HAS_WHITENOISE = importlib.util.find_spec("whitenoise") is not None
ON_RENDER = bool(os.getenv("RENDER")) or bool(os.getenv("RENDER_EXTERNAL_HOSTNAME"))
LOCAL_STAGING = _env_bool("DJANGO_LOCAL_STAGING", False)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key-change-me")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = _env_bool("DJANGO_DEBUG", not ON_RENDER)

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1,brainiacs-site.onrender.com,brainiacs.academy,www.brainiacs.academy"
).split(",")
CSRF_TRUSTED_ORIGINS = _env_list("DJANGO_CSRF_TRUSTED_ORIGINS", "")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'landing.apps.LandingConfig',
    'levels',
    'lessons'  # Replace with your actual app name
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'brainiacs_site.middleware.SiteLanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'brainiacs_site.middleware.LessonsLoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if HAS_WHITENOISE:
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

ROOT_URLCONF = 'brainiacs_site.urls'  # Make sure this matches your project folder

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # If you have custom template dirs, add them here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'brainiacs_site.wsgi.application'

# Database
if dj_database_url:
    # Defaults to SQLite locally, uses DATABASE_URL in hosting environments.
    DATABASES = {
        "default": dj_database_url.config(
            default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
            if (not DEBUG and HAS_WHITENOISE and not LOCAL_STAGING)
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
    },
}

# Media files (not used for icons anymore, but still good to have)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_PROVIDER = _env_first(("EMAIL_PROVIDER",), default="smtp").strip().lower()
SENDGRID_API_KEY = _env_first(("SENDGRID_API_KEY",), default="")

if EMAIL_PROVIDER == "sendgrid" or SENDGRID_API_KEY:
    EMAIL_PROVIDER = "sendgrid"
    EMAIL_BACKEND = _env_first(
        ("EMAIL_BACKEND", "DJANGO_EMAIL_BACKEND"),
        default="django.core.mail.backends.smtp.EmailBackend",
    )
    EMAIL_HOST = _env_first(
        ("EMAIL_HOST", "DJANGO_EMAIL_HOST"),
        default="smtp.sendgrid.net",
    )
    EMAIL_PORT = _env_int_first(("EMAIL_PORT", "DJANGO_EMAIL_PORT"), default=587)
    EMAIL_USE_TLS = _env_bool_first(
        ("EMAIL_USE_TLS", "DJANGO_EMAIL_USE_TLS"),
        default=True,
    )
    EMAIL_HOST_USER = _env_first(
        ("EMAIL_HOST_USER", "DJANGO_EMAIL_HOST_USER"),
        default="apikey",
    )
    EMAIL_HOST_PASSWORD = _env_first(
        ("EMAIL_HOST_PASSWORD", "DJANGO_EMAIL_HOST_PASSWORD"),
        default=SENDGRID_API_KEY,
    )
else:
    EMAIL_PROVIDER = "smtp"
    EMAIL_BACKEND = _env_first(
        ("EMAIL_BACKEND", "DJANGO_EMAIL_BACKEND"),
        default="django.core.mail.backends.smtp.EmailBackend",
    )
    EMAIL_HOST = _env_first(("EMAIL_HOST", "DJANGO_EMAIL_HOST"), default="")
    EMAIL_PORT = _env_int_first(("EMAIL_PORT", "DJANGO_EMAIL_PORT"), default=587)
    EMAIL_USE_TLS = _env_bool_first(
        ("EMAIL_USE_TLS", "DJANGO_EMAIL_USE_TLS"),
        default=True,
    )
    EMAIL_HOST_USER = _env_first(
        ("EMAIL_HOST_USER", "DJANGO_EMAIL_HOST_USER"),
        default="",
    )
    EMAIL_HOST_PASSWORD = _env_first(
        ("EMAIL_HOST_PASSWORD", "DJANGO_EMAIL_HOST_PASSWORD"),
        default="",
    )
EMAIL_TIMEOUT = _env_int_first(("EMAIL_TIMEOUT", "DJANGO_EMAIL_TIMEOUT"), default=12)
DEFAULT_FROM_EMAIL = _env_first(
    ("DEFAULT_FROM_EMAIL", "DJANGO_DEFAULT_FROM_EMAIL"),
    default="Brainiacs <no-reply@brainiacs.academy>",
)
SERVER_EMAIL = _env_first(("SERVER_EMAIL",), default=DEFAULT_FROM_EMAIL)
BRAINIACS_OUTBOUND_FROM_EMAIL = os.getenv(
    "BRAINIACS_OUTBOUND_FROM_EMAIL",
    EMAIL_HOST_USER or DEFAULT_FROM_EMAIL,
)
BRAINIACS_SUPPORT_EMAIL = os.getenv(
    "BRAINIACS_SUPPORT_EMAIL",
    "hello@brainiacs.academy",
)
BRAINIACS_EMAIL_CONFIRM_TOKEN_MAX_AGE = int(
    os.getenv("BRAINIACS_EMAIL_CONFIRM_TOKEN_MAX_AGE", "86400")
)
BRAINIACS_LOGIN_ALERT_COOLDOWN_SECONDS = _env_int_first(
    ("BRAINIACS_LOGIN_ALERT_COOLDOWN_SECONDS",),
    default=60 * 60 * 12,
)
SITE_URL = _env_first(
    ("SITE_URL", "DJANGO_SITE_URL"),
    default="http://127.0.0.1:8000",
).rstrip("/")

if DEBUG and not EMAIL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if (
    (not DEBUG)
    and EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend"
    and not EMAIL_HOST
):
    raise ImproperlyConfigured(
        "EMAIL_HOST is not set. Configure SMTP env vars on Render."
    )
if (
    (not DEBUG)
    and EMAIL_PROVIDER == "sendgrid"
    and EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend"
    and not EMAIL_HOST_PASSWORD
):
    raise ImproperlyConfigured(
        "SENDGRID_API_KEY (or EMAIL_HOST_PASSWORD) is not set for SendGrid provider."
    )

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/lessons/'
LOGOUT_REDIRECT_URL = '/auth/login/'

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# Render/proxy deployments can forward host headers; keep local behavior configurable.
USE_X_FORWARDED_HOST = _env_bool("DJANGO_USE_X_FORWARDED_HOST", ON_RENDER)

if not DEBUG and not LOCAL_STAGING:
    SECURE_SSL_REDIRECT = _env_bool("DJANGO_SECURE_SSL_REDIRECT", True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "brainiacs.email": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        }
    },
}
