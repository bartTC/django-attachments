import os

DEBUG = True

TESTAPP_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "testsecretkey"

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "tests.db"}
}

MEDIA_ROOT = os.path.join(TESTAPP_DIR, "uploads")
ROOT_URLCONF = "attachments.tests.testapp.urls"

INSTALLED_APPS = [
    "attachments",
    "attachments.tests.testapp",
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
