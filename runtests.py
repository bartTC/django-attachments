#!/usr/bin/env python

import sys

from django import setup
from django.conf import settings
from django.test.runner import DiscoverRunner

def runtests(*test_args):
    # Setup settings
    if not settings.configured:
        from attachments.tests.testapp import settings as TEST_SETTINGS
        settings.configure(**TEST_SETTINGS.__dict__)

    setup()

    test_runner = DiscoverRunner(verbosity=1)
    failures = test_runner.run_tests(['attachments'])
    if failures:
        sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])
