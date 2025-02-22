import sys
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
print(f"BASE_DIR is {BASE_DIR}")
environ.Env.read_env(BASE_DIR / ".env")
env = environ.Env()

DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_vite",
    "rest_framework",
    "rest_framework_api_key",
    "django_filters",
    "slippers",
    "backend.users",
    "backend.core",
    "backend.zettle",
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
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3333",  # Vue dev server
]


ROOT_URLCONF = "backend.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "backend" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": ["slippers.templatetags.slippers"],
        },
    },
]


WSGI_APPLICATION = "backend.wsgi.application"


DATABASES = {
    "default": env.db("DATABASE_URL", default="sqlite:///recursivegarden.db"),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

CRISPY_FAIL_SILENTLY = False
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "users.User"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [
    BASE_DIR / "backend" / "static",
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_ROOT = BASE_DIR / "backend" / "media"
MEDIA_URL = "/media/"


REST_FRAMEWORK = {
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    # "DEFAULT_AUTHENTICATION_CLASSES": [
    #    "rest_framework.authentication.SessionAuthentication",
    # ],
    # "DEFAULT_PERMISSION_CLASSES": [
    #    "rest_framework_api_key.permissions.HasAPIKey",
    #    "rest_framework.permissions.IsAuthenticated",
    # ],
}

X_FRAME_OPTIONS = "SAMEORIGIN"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DJANGO_ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/").strip("/")
ADMINS = [
    ("David Colgan", "david@recursivegarden.com"),
]
SERVER_EMAIL = "david@recursivegarden.com"

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    POSTMARK_API_KEY = env("POSTMARK_API_KEY")

    EMAIL_HOST = "smtp.postmarkapp.com"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = POSTMARK_API_KEY
    EMAIL_HOST_PASSWORD = POSTMARK_API_KEY
    EMAIL_USE_TLS = True


INTERNAL_IPS = [
    "127.0.0.1",
]


DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
        "dev_server_port": 3333,
    },
}

if DEBUG:
    ALLOWED_HOSTS = ["*"]
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    print("Settings are: DEV")

if "test" in sys.argv:
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    print("Settings are: TESTING")
