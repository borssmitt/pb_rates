from pathlib import Path
import os

# --- Основные настройки ---
BASE_DIR = Path(__file__).resolve().parent.parent  # 🔹 ЭТО ВАЖНО: иначе BASE_DIR будет не определён

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret")
DEBUG = True
ALLOWED_HOSTS = ["*"]

# --- Приложения ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rates",  # твоё приложение
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- URLs и шаблоны ---
ROOT_URLCONF = "pb_rates.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Папка templates в корне проекта
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

# --- Две базы данных ---
DATABASES = {
    "default": {  # Для системных нужд Django
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "rates_db": {  # Для модели Rate — PostgreSQL
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("RATES_DB_NAME", "rates_db"),
        "USER": os.getenv("RATES_DB_USER", "rates_user"),
        "PASSWORD": os.getenv("RATES_DB_PASSWORD", "rates_password"),
        "HOST": os.getenv("RATES_DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("RATES_DB_PORT", "5432"),
    },
}

# --- Роутер для маршрутизации модели Rate в отдельную базу ---
DATABASE_ROUTERS = ["pb_rates.dbrouters.RatesRouter"]

# --- Статика ---
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# --- Локаль и часовой пояс ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True
