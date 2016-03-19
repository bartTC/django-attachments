#!/usr/bin/env python
import sys

from django.conf import settings

SETTINGS = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'dev.db',
        },
        # 'default': {
        #     'ENGINE': 'django.db.backends.mysql',
        #     'NAME': 'dpaste',
        #     'USER': 'root',
        #     'PASSWORD': '',
        # }
    },
    'ROOT_URLCONF': 'attachments.tests.MyTestProject.urls',
    'INSTALLED_APPS': [
        'attachments',
        'attachments.tests.MyTestProject',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',

    ],
    'MIDDLEWARE_CLASSES': (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ),
}

def runtests(*test_args):
    # Setup settings
    if not settings.configured:
        settings.configure(**SETTINGS)

    # New Django 1.7 app registry setup
    try:
        from django import setup
        setup()
    except ImportError:
        pass

    # New Django 1.8 test runner
    try:
        from django.test.runner import DiscoverRunner as TestRunner
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner as TestRunner

    test_runner = TestRunner(verbosity=1)
    failures = test_runner.run_tests(['attachments'])
    if failures:
        sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])
