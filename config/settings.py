import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name: str, default: bool = False) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


# SECURITY
SECRET_KEY = (
    os.environ.get("DJANGO_SECRET_KEY")
    or os.environ.get("SECRET_KEY")
    or "dev-secret-key-change-me"
)

DEBUG = env_bool("DJANGO_DEBUG", default=env_bool("DEBUG", default=False))

# Hosts (Render + lokal)
_allowed = {"127.0.0.1", "localhost", ".onrender.com"}

# Render setzt oft RENDER_EXTERNAL_HOSTNAME (z.B. portfolio-m7bv.onrender.com)
render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    _allowed.add(render_host)

extra_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS") or os.environ.get("ALLOWED_HOSTS") or ""
if extra_hosts:
    for h in extra_hosts.split(","):
        h = h.strip()
        if h:
            _allowed.add(h)

ALLOWED_HOSTS = sorted(_allowed)


# APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "portfolio",
]

# MIDDLEWARE
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"


# DATABASE (SQLite: Achtung -> auf Render ohne Disk nicht persistent!)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "de"
TIME_ZONE = "Europe/Zurich"
USE_I18N = True
USE_TZ = True


# STATIC
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]


# MEDIA (lokal ok; auf Render ohne Cloudinary wird /media nicht funktionieren)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# STORAGES (Django 5+)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
    # "default" setzen wir unten abhängig von CLOUDINARY_URL
}


# Cloudinary (wenn CLOUDINARY_URL gesetzt ist -> Media laufen über Cloudinary)
CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL", "").strip()
if CLOUDINARY_URL:
    INSTALLED_APPS += ["cloudinary", "cloudinary_storage"]
    STORAGES["default"] = {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"
    }
else:
    STORAGES["default"] = {
        "BACKEND": "django.core.files.storage.FileSystemStorage"
    }


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Render / HTTPS
CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com"]
if render_host:
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_host}")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
