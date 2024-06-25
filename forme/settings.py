import datetime
import os
import environ
from pathlib import Path
from datetime import timedelta

# set casting, default value
env = environ.Env(DEBUG=(bool, False))  # <-- Updated!

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(BASE_DIR / ".env")  # <-- Updated!

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/reecklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env("SECRET_KEY")  # <-- Updated!
SECRET_KEY = "django-insecure-jv3b&ixles^8cm-(af_$0m@_)y)79ew6gdm$5i4u^#)yh=wm$k"
# SECRET_KEY = "django-insecure-jv3b&ixles^8cm-(af_$0m@_)y)79ew6gdm$5i4u^#)yh=wm$k"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = "True"  # <-- Updated!

if DEBUG:
    INTERNAL_IPS = ["127.0.0.1"]  # <-- Updated!


ALLOWED_HOSTS = ["127.0.0.1", "192.168.1.3", "forme-app-7pffc.ondigitalocean.app"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "django_better_admin_arrayfield",
    "corsheaders",
    "drf_yasg",
    "authentication",
    "clubs",
    "trainings",
    "social_auth",
    "debug_toolbar",  # <-- Updated!,
    "django_celery_beat",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # <-- Updated!
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "forme.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "forme.wsgi.application"

# CORS WHITELIST
CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:8080",
]


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Database Configuration
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
    }
}

POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    # "EXCEPTION_HANDLER": "authentication.utils.custom_exception_handler",
}
# SWAGGER_SETTINGS = {
#     "SECURITY_DEFINITIONS": {
#         "Bearer": {
#             "type": "apiKey",
#             "name": "Authorization",
#             "in": "header",
#         }
#     }
# }

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=365),  # Set to 1 year
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=365),  # Set to 1 year
}

DEBUG_TOOLBAR_CONFIG = {"IS_RUNNING_TESTS": False}

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://localhost:6379/",
#         "KEY_PREFIX": "imdb",
#         "TIMEOUT": 60 * 15,  # in seconds: 60 * 15 (15 minutes)
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     }
# }

# Optionally, you can configure Django Channels to use Redis as well
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": ["redis://localhost:6379/"],
#         },
#     },
# }

# Optionally, you can configure Django Sessions to use Redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Cairo"

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "authentication.CustomUser"

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = "media/hussein/H.salem/fci_2020/computer_programming/Graduation_Project/Forme_API/static/"
STATIC_URL = "/static/"
STATICFILES_DIR = [os.path.join(BASE_DIR, "/static")]

# Default primary key field types
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEMPLATES_BASE_URL = "http://127.0.0.1:8000"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
Email_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = (
    "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"
)
DEFAULT_FROM_EMAIL = "husseinsalem910@gmail.com"
DEFAULT_HOST_PASSWORD = (
    "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"
)


SENDGRID_API_KEY = (
    "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"
)
SENDGRID_FROM_EMAIL = "husseinsalem910@gmail.com"

# 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

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# Email_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "salemhussein49@gmail.com"
# EMAIL_HOST_PASSWORD = "qtcd vzge nqex joph"

CORS_ALLOWED_ORIGINS = [
    "http://10.0.2.2:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://localhost:3001",
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = False

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]


# CELERY SETTINGS
CELERY_BACKEND = 'redis://localhost:6379/3'
CELERY_BROKER_URL = 'redis://localhost:6379/4'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/5'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_ENABLE_UTC = True

BASE_URL="https://forme-app-7pffc.ondigitalocean.app/"
# CELERY_BEAT_SCHEDULE = {
#     "create-daily-attendance": {
#         "task": "clubs.tasks.create_daily_attendance",
#         "schedule": timedelta(days=1),
#     },
# }
