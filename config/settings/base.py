from pathlib import Path

from .constants import (
    AUTH_VALIDATORS,
    DJANGO_APPS,
    MIDDLEWARE_CLASSES,
    PROJECT_APPS,
    TEMPLATE_CONTEXT_PROCESSORS,
    THIRD_PARTY_APPS,
)
from .env import Env

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

env = Env()

# --- Core ---

SECRET_KEY: str = env.require("DJANGO_SECRET_KEY")
DEBUG: bool = env.get_bool("DJANGO_DEBUG")
ALLOWED_HOSTS: list[str] = env.get_list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS: list[str] = env.get_list("CSRF_TRUSTED_ORIGINS")
APP_BASE_URL: str = env.get_str("APP_BASE_URL", "http://localhost:8000")

# --- Apps ---

INSTALLED_APPS: list[str] = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

# --- Middleware ---

MIDDLEWARE: list[str] = MIDDLEWARE_CLASSES

# --- URLs & WSGI ---

ROOT_URLCONF: str = "config.urls"
WSGI_APPLICATION: str = "config.wsgi.application"

# --- Templates ---

TEMPLATES: list[dict[str, str | list[Path] | bool | dict[str, list[str]]]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": TEMPLATE_CONTEXT_PROCESSORS,
        },
    },
]

# --- Database ---
# Production DATABASE_URL must include ?sslmode=require for DigitalOcean managed PostgreSQL.
# PostgreSQL connections default to sslmode=require if not specified in the URL.

DATABASES = {
    "default": env.database_url(),
}

# --- Auth ---

AUTH_PASSWORD_VALIDATORS = AUTH_VALIDATORS

# --- i18n ---

LANGUAGE_CODE: str = "he"
TIME_ZONE: str = "Asia/Jerusalem"
USE_I18N: bool = True
USE_TZ: bool = True

# --- Static files ---

STATIC_URL: str = "static/"
STATIC_ROOT: Path = BASE_DIR / "staticfiles"
STATICFILES_DIRS: list[Path] = [BASE_DIR / "static"]
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- Email ---

EMAIL_HOST: str = env.get_str("EMAIL_HOST", "localhost")
EMAIL_PORT: int = env.get_int("EMAIL_PORT", default=587)
EMAIL_USE_TLS: bool = env.get_bool("EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL: bool = env.get_bool("EMAIL_USE_SSL", default=False)
EMAIL_HOST_USER: str = env.get_str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD: str = env.get_str("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL: str = env.get_str("DEFAULT_FROM_EMAIL", "noreply@larp.co.il")

# --- Cardcom ---

CARDCOM_TERMINAL_NUMBER: str = env.get_str("CARDCOM_TERMINAL_NUMBER")
CARDCOM_API_NAME: str = env.get_str("CARDCOM_API_NAME")
CARDCOM_API_PASSWORD: str = env.get_str("CARDCOM_API_PASSWORD")
CARDCOM_LOW_PROFILE_URL: str = env.get_str(
    "CARDCOM_LOW_PROFILE_URL",
    "https://secure.cardcom.solutions/api/v11/LowProfile/Create",
)
CARDCOM_GET_LP_RESULT_URL: str = env.get_str(
    "CARDCOM_GET_LP_RESULT_URL",
    "https://secure.cardcom.solutions/api/v11/LowProfile/GetLpResult",
)

# --- Misc ---

DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"
