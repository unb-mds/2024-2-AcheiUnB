import os
from datetime import timedelta
from pathlib import Path

import cloudinary
import cloudinary.uploader
from celery.schedules import crontab
from decouple import config

if os.getenv("DJANGO_SETTINGS_MODULE") == "AcheiUnB.settings_production":
    from .settings_production import *

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-%7=()&6sxvzdq68n)q^8n)g6#kw8p=45v)(hp^t%@*e4ty=##u"

DEBUG = True

ALLOWED_HOSTS = ["*"]
AUTH_USER_MODEL = "auth.User"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_filters",
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
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]


ROOT_URLCONF = "AcheiUnB.urls"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("users.authentication.CookieJWTAuthentication",),
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 27,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365 * 10),
    "SIGNING_KEY": SECRET_KEY,
    "ALGORITHM": "HS256",
}

ASGI_APPLICATION = "AcheiUnB.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.channels_redis",  # Para desenvolvimento local
        # "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "AcheiUnB.wsgi.application"

SOCIALACCOUNT_PROVIDERS = {
    "microsoft": {
        "APP": {
            "client_id": os.getenv("MICROSOFT_CLIENT_ID"),
            "secret": os.getenv("MICROSOFT_CLIENT_SECRET"),
            "authority": os.getenv("MICROSOFT_AUTHORITY"),
            "key": "",
        },
    }
}
MICROSOFT_REDIRECT_URI = "http://localhost:8000/accounts/microsoft/login/callback/"
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS["microsoft"]["AUTH_PARAMS"] = {
    "domain": "alunos.unb.br",
}
SOCIALACCOUNT_PROVIDERS["microsoft"]["SCOPE"] = [
    "email",
    "openid",
    "profile",
    "User.Read",
]

ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"
SOCIALACCOUNT_ADAPTER = "allauth.socialaccount.adapter.DefaultSocialAccountAdapter"
SOCIALACCOUNT_ADAPTER = "users.adapters.CustomSocialAccountAdapter"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


cloudinary.config(
    CLOUDINARY_CLOUD_NAME=os.getenv("CLOUDINARY_CLOUD_NAME"),
    CLOUDINARY_API_KEY=os.getenv("CLOUDINARY_API_KEY"),
    CLOUDINARY_API_SECRET=os.getenv("CLOUDINARY_API_SECRET"),
)


EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=587)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="acheiunb2024@gmail.com")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "AcheiUnB/static/dist"),
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1
LOGIN_REDIRECT_URL = "/certu"
LOGOUT_REDIRECT_URL = ""
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"
LANGUAGE_CODE = "pt-br"

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

CELERY_BEAT_SCHEDULE = {
    "delete_old_items_and_chats": {
        "task": "users.tasks.delete_old_items_and_chats",
        "schedule": crontab(hour=3, minute=0),
    },
}

INSTALLED_APPS += ["django_celery_results"]


JAZZMIN_SETTINGS = {
    "site_title": "AcheiUnB Admin",
    "site_header": "AcheiUnB",
    "welcome_sign": "Bem-vindo ao painel do AcheiUnB!",
    "search_model": "auth.User",
    "user_avatar": None,
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "custom_links": {
        "users": [
            {
                "name": "Celery Tasks",
                "url": "/admin/django_celery_results/taskresult/",
                "icon": "fas fa-tasks",
            }
        ],
    },
}
