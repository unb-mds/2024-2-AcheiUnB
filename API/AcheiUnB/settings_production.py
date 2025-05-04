import os
from pathlib import Path

from .settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

ALLOWED_HOSTS = ["achadoseperdidos.lappis.rocks", "acheiunb.com.br", "localhost", "127.0.0.1"]
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "users",
    "rest_framework",
    "rest_framework.authtoken",
    "AcheiUnB",
    "django_extensions",
    "channels",
    "chat",
    "corsheaders",
    "django_celery_beat",
    "drf_yasg",
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",  # Necessário para o admin
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Necessário para o admin
    "django.contrib.messages.middleware.MessageMiddleware",  # Necessário para o admin
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("users.authentication.CookieJWTAuthentication",),
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 27,
}


BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "users" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "AcheiUnB/static/dist"),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


SECRET_KEY = "django-insecure-%7=()&6sxvzdq68n)q^8n)g6#kw8p=45v)(hp^t%@*e4ty=##u"

CORS_ALLOWED_ORIGINS = [
    "https://localhost:8080",
    "https://127.0.0.1:8080",
]
CORS_ALLOW_CREDENTIALS = True  # Permite cookies na autenticação
CORS_ALLOW_HEADERS = ["*"]
CORS_ALLOW_METHODS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    "https://localhost:8080",
    "https://127.0.0.1:8080",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
ROOT_URLCONF = "AcheiUnB.urls"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "/var/log/django/error.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
LOGOUT_REDIRECT_URL = "https://localhost:8080/#/"  # Para desenvolvimento
# LOGOUT_REDIRECT_URL = "https://achadoseperdidos.lappis.rocks/#/"  # Para produção
LOGIN_REDIRECT_URL = "https://localhost:8080/#/lost"  # Para desenvolvimento
# LOGIN_REDIRECT_URL = "https://achadoseperdidos.lappis.rocks/#/lost"  # Para produção
