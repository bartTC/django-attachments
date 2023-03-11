import os

DEBUG = True

TESTAPP_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "testsecretkey"

if os.environ.get("DJANGO_DATABASE_ENGINE") == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "USER": "postgres",
            "NAME": "attachments",
            "HOST": "localhost",
            "PORT": 5432,
        }
    }
elif os.environ.get("DJANGO_DATABASE_ENGINE") == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "USER": "root",
            "NAME": "attachments",
            "HOST": "127.0.0.1",
            "PORT": 3306,
        }
    }
else:
    DATABASES = {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "tests.db"}
    }

DATABASES["default"].update(
    {
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", "testing"),
    }
)

MEDIA_ROOT = os.path.join(TESTAPP_DIR, "uploads")
ROOT_URLCONF = "attachments.tests.testapp.urls"

INSTALLED_APPS = [
    "attachments.tests.testapp",
    "attachments.tests.testapp.apps.CustomizedAttachmentsApp",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
]

MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(TESTAPP_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
