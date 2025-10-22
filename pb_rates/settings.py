from pathlib import Path
import os
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret")
DEBUG = True
ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
"django.contrib.admin",
"django.contrib.auth",
"django.contrib.contenttypes",
"django.contrib.sessions",
"django.contrib.messages",
"django.contrib.staticfiles",
"rates",
]


MIDDLEWARE = [
"django.middleware.security.SecurityMiddleware",
"django.contrib.sessions.middleware.SessionMiddleware",
"django.middleware.common.CommonMiddleware",
"django.middleware.csrf.CsrfViewMiddleware",
"django.contrib.auth.middleware.AuthenticationMiddleware",
"django.contrib.messages.middleware.MessageMiddleware",
"django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "pb_rates.urls"
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


WSGI_APPLICATION = "pb_rates.wsgi.application"


# ---- Two separate databases (default + dedicated 'rates_db') ----
DATABASES = {
"default": { # keep this for Django itself (auth/sessions). Can be SQLite.
"ENGINE": "django.db.backends.sqlite3",
"NAME": BASE_DIR / "db.sqlite3",
},
"rates_db": { # PostgreSQL database ONLY for Rate snapshots
"ENGINE": "django.db.backends.postgresql",
"NAME": os.getenv("RATES_DB_NAME", "rates_db"),
"USER": os.getenv("RATES_DB_USER", "rates_user"),
"PASSWORD": os.getenv("RATES_DB_PASSWORD", "rates_password"),
"HOST": os.getenv("RATES_DB_HOST", "127.0.0.1"),
"PORT": os.getenv("RATES_DB_PORT", "5432"),
},
}


# Route the Rate model to rates_db
DATABASE_ROUTERS = ["pb_rates.dbrouters.RatesRouter"]


# Static
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]


# Timezone
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True