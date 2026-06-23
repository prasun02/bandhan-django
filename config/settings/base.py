import os
import importlib.util
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

try:
    import dj_database_url
except ImportError:
    dj_database_url = None

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False


# =========================================================
# BASE DIRECTORY AND ENVIRONMENT FILE
# =========================================================

# Project structure:
#
# BANDHAN-DJANGO/
# ├── config/
# │   └── settings/
# │       └── base.py
# ├── templates/
# ├── static/
# ├── media/
# ├── manage.py
# └── .env

BASE_DIR = Path(__file__).resolve().parents[2]

# Load environment variables from the project-root .env file.
load_dotenv(BASE_DIR / ".env")


# =========================================================
# ENVIRONMENT HELPERS
# =========================================================

def env(name, default=None, required=False):
    """
    Read a single environment variable.

    Example:
        SECRET_KEY = env("SECRET_KEY", required=True)
    """
    value = os.environ.get(name, default)

    if required and value in (None, ""):
        raise ImproperlyConfigured(
            f"Missing required environment variable: {name}"
        )

    return value


def env_bool(name, default=False):
    """
    Read a Boolean environment variable.

    Accepted true values:
        true, 1, yes, on
    """
    value = env(name, str(default))

    if isinstance(value, bool):
        return value

    return str(value).strip().lower() in {
        "true",
        "1",
        "yes",
        "on",
    }


def env_int(name, default=0):
    """
    Read an integer environment variable.
    """
    value = env(name, default)

    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ImproperlyConfigured(
            f"Environment variable {name} must be an integer."
        ) from exc


def env_list(name, default=""):
    """
    Read a comma-separated environment variable as a list.

    Example:
        ALLOWED_HOSTS=localhost,127.0.0.1
    """
    value = env(name, default)

    if isinstance(value, (list, tuple)):
        return list(value)

    return [
        item.strip()
        for item in str(value).split(",")
        if item.strip()
    ]


# =========================================================
# CORE DJANGO SETTINGS
# =========================================================

SECRET_KEY = env(
    "SECRET_KEY",
    "development-insecure-change-me",
)

DEBUG = env_bool("DEBUG", default=False)

ALLOWED_HOSTS = env_list(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1",
)

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    "",
)

SITE_ID = 1


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    # Django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",

    # Bandhan applications
    "accounts",
    "catalog",
    "cart",
    "checkout",
    "orders",
    "payments",
    "shipping",
    "promotions",
    "reviews",
    "returns",
    "core",
    "dashboard",
    "notifications",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if importlib.util.find_spec("whitenoise"):
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")


# =========================================================
# URL, WSGI AND ASGI
# =========================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": (
            "django.template.backends.django.DjangoTemplates"
        ),
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                (
                    "django.template.context_processors.debug"
                ),
                (
                    "django.template.context_processors.request"
                ),
                (
                    "django.contrib.auth.context_processors.auth"
                ),
                (
                    "django.contrib.messages."
                    "context_processors.messages"
                ),
                "core.context_processors.brand",
                "cart.context_processors.cart_summary",
            ],
        },
    },
]


# =========================================================
# AUTHENTICATION
# =========================================================

AUTH_USER_MODEL = "accounts.User"

LOGIN_URL = "accounts:login"

LOGIN_REDIRECT_URL = "accounts:dashboard"

LOGOUT_REDIRECT_URL = "home"


# =========================================================
# DATABASE
# =========================================================

# Local computer:
# If DATABASE_URL is empty or missing, Django uses SQLite.
#
# Live Render/Neon:
# If DATABASE_URL exists, Django uses the online database.

DATABASE_URL = env("DATABASE_URL", "").strip()


if DATABASE_URL:
    if dj_database_url is None:
        raise ImproperlyConfigured(
            "DATABASE_URL requires dj-database-url. Install requirements.txt first."
        )
    database_config = dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=60,
    )

    database_engine = database_config.get("ENGINE", "")

    # Check old database connections before reusing them.
    database_config["CONN_HEALTH_CHECKS"] = True

    # Recommended for PostgreSQL connection poolers and
    # serverless databases such as Neon.
    if database_engine.endswith("postgresql"):
        database_config["DISABLE_SERVER_SIDE_CURSORS"] = True

        # Require SSL for production PostgreSQL unless explicitly
        # disabled through DATABASE_SSL_REQUIRED=False.
        if env_bool(
            "DATABASE_SSL_REQUIRED",
            default=not DEBUG,
        ):
            database_config.setdefault("OPTIONS", {})
            database_config["OPTIONS"].setdefault(
                "sslmode",
                "require",
            )

    # MySQL/MariaDB configuration.
    if database_engine.endswith("mysql"):
        database_config.setdefault("OPTIONS", {})
        database_config["OPTIONS"].setdefault(
            "charset",
            "utf8mb4",
        )

    DATABASES = {
        "default": database_config,
    }

else:
    # Local SQLite database.
    # PostgreSQL installation and pgAdmin are not required.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =========================================================
# LANGUAGE AND TIME
# =========================================================

LANGUAGE_CODE = env(
    "LANGUAGE_CODE",
    "en-us",
)

TIME_ZONE = env(
    "TIME_ZONE",
    "Asia/Dhaka",
)

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# =========================================================
# MEDIA FILES
# =========================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# STORAGE
# =========================================================

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

if importlib.util.find_spec("whitenoise"):
    STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# =========================================================
# EMAIL
# =========================================================

EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)

EMAIL_HOST = env(
    "EMAIL_HOST",
    "",
)

EMAIL_PORT = env_int(
    "EMAIL_PORT",
    587,
)

EMAIL_HOST_USER = env(
    "EMAIL_HOST_USER",
    "",
)

EMAIL_HOST_PASSWORD = env(
    "EMAIL_HOST_PASSWORD",
    "",
)

EMAIL_USE_TLS = env_bool(
    "EMAIL_USE_TLS",
    default=True,
)

EMAIL_USE_SSL = env_bool(
    "EMAIL_USE_SSL",
    default=False,
)

DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL",
    "Bandhan <noreply@example.com>",
)

SERVER_EMAIL = env(
    "SERVER_EMAIL",
    DEFAULT_FROM_EMAIL,
)


# =========================================================
# SESSION AND COOKIE SECURITY
# =========================================================

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SAMESITE = "Lax"

SESSION_COOKIE_SECURE = env_bool(
    "SESSION_COOKIE_SECURE",
    default=not DEBUG,
)

CSRF_COOKIE_SECURE = env_bool(
    "CSRF_COOKIE_SECURE",
    default=not DEBUG,
)


# =========================================================
# HTTPS AND SECURITY HEADERS
# =========================================================

SECURE_SSL_REDIRECT = env_bool(
    "SECURE_SSL_REDIRECT",
    default=False,
)

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

USE_X_FORWARDED_HOST = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_REFERRER_POLICY = (
    "strict-origin-when-cross-origin"
)

X_FRAME_OPTIONS = "DENY"

SECURE_HSTS_SECONDS = env_int(
    "SECURE_HSTS_SECONDS",
    0,
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=False,
)

SECURE_HSTS_PRELOAD = env_bool(
    "SECURE_HSTS_PRELOAD",
    default=False,
)


# =========================================================
# FILE UPLOAD LIMITS
# =========================================================

# 10 MB maximum in-memory upload.
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# 15 MB maximum total request body.
DATA_UPLOAD_MAX_MEMORY_SIZE = 15 * 1024 * 1024


# =========================================================
# CACHE
# =========================================================

CACHES = {
    "default": {
        "BACKEND": (
            "django.core.cache.backends.locmem."
            "LocMemCache"
        ),
        "LOCATION": "bandhan-local-cache",
    }
}


# =========================================================
# LOGGING
# =========================================================

LOG_LEVEL = env(
    "LOG_LEVEL",
    "INFO",
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": (
                "{levelname} {asctime} "
                "{name} {message}"
            ),
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": [
            "console",
        ],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "django": {
            "handlers": [
                "console",
            ],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# BANDHAN BUSINESS SETTINGS
# =========================================================

BANDHAN_BUSINESS_NAME = env(
    "BANDHAN_BUSINESS_NAME",
    "Bandhan",
)

BANDHAN_TAGLINE = env(
    "BANDHAN_TAGLINE",
    "Tradition Woven with Elegance",
)

BANDHAN_CONTACT_PHONE = env(
    "BANDHAN_CONTACT_PHONE",
    "+880 1700-000000",
)

BANDHAN_CONTACT_EMAIL = env(
    "BANDHAN_CONTACT_EMAIL",
    "support@example.com",
)

# Do not place a comma after this value.
BANDHAN_CURRENCY_SYMBOL = "৳"


# =========================================================
# PAYMENT FEATURE FLAGS
# =========================================================

BKASH_ENABLED = env_bool(
    "BKASH_ENABLED",
    default=False,
)

CCARD_PAYMENT_ENABLED = env_bool(
    "CARD_PAYMENT_ENABLED",
    default=False,
)
