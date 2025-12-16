import os
import dj_database_url
from .settings import *

DEBUG = False

# Hosts
ALLOWED_HOSTS = [
    os.environ.get("RENDER_EXTERNAL_HOSTNAME"),
    "shipmanage.onrender.com"
]

CSRF_TRUSTED_ORIGINS = [
    f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}",
    "https://shipmanage.onrender.com",
]

SECRET_KEY = os.environ.get("SECRET_KEY")

# --------------------------
# ⭐ CORS SETTINGS (THE FIX)
# --------------------------
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "https://shipmanage-r.onrender.com",
]

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------
# STATIC FILES
# --------------------------
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

# --------------------------
# DATABASE (RENDER)
# --------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
    )
}
