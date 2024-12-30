import os
from pathlib import Path
from datetime import timedelta
import cloudinary
import cloudinary.uploader
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%7=()&6sxvzdq68n)q^8n)g6#kw8p=45v)(hp^t%@*e4ty=##u"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
AUTH_USER_MODEL = "auth.User"
MEDIA_URL = "/media/"  # Prefixo da URL para os arquivos
MEDIA_ROOT = os.path.join(
    BASE_DIR, "/home/pedroubu/Imagens/AcheiUnBFt"
)  # Diretório onde os arquivos serão salvos

# Application definition

INSTALLED_APPS = [
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
    "AcheiUnB",
    "django_extensions",
    "channels",
    "chat",
    "corsheaders",
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
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",  # Apenas JSON será usado
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SIGNING_KEY": SECRET_KEY,  # Use a chave secreta do Django
    "ALGORITHM": "HS256",
}

ASGI_APPLICATION = "AcheiUnB.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.channels_redis",  # Para desenvolvimento local
        "BACKEND": "channels.layers.InMemoryChannelLayer",
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

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

CORS_ALLOW_ALL_ORIGINS = True


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

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
