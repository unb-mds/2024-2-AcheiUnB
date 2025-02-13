import os
from datetime import timedelta
from pathlib import Path

import cloudinary
import cloudinary.uploader
from celery.schedules import crontab
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%7=()&6sxvzdq68n)q^8n)g6#kw8p=45v)(hp^t%@*e4ty=##u"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ["achadoseperdidos.lappis.rocks", "www.achadoseperdidos.lappis.rocks", "localhost", "127.0.0.1"]
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# 🔹 Configuração do CSRF e CORS
CSRF_TRUSTED_ORIGINS = ["https://achadoseperdidos.lappis.rocks"]
CORS_ALLOWED_ORIGINS = ["https://achadoseperdidos.lappis.rocks"]

AUTH_USER_MODEL = "auth.User"
MEDIA_URL = "/media/"  # Prefixo da URL para os arquivos
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # Diretório onde os arquivos serão salvos

# Application definition

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
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "users.authentication.CookieJWTAuthentication",  # Caminho do módulo e classe
    ),
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",  # Apenas JSON será usado
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
# Permitir apenas usuários do tenant da UnB
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


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

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

# Cloudinary


cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET"),
)


# Envio de mensagens

EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=587)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="acheiunb2024@gmail.com")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "AcheiUnB/static/dist"),  # Diretório dos arquivos do Vue.js
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1
LOGIN_REDIRECT_URL = "/certu"
LOGOUT_REDIRECT_URL = ""
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"
LANGUAGE_CODE = "pt-br"


# Configurações do Celery
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# Backend para armazenar resultados (opcional)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

# Celery Beat Configuration
CELERY_BEAT_SCHEDULE = {
    "delete_old_items_and_chats": {
        "task": "users.tasks.delete_old_items_and_chats",
        "schedule": crontab(hour=3, minute=0),
    },
}

# Configurações do Django celery results
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
