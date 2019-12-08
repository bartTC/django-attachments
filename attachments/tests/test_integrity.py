from django.core.management import call_command
from django.test import TestCase
from six import StringIO


class IntegrityTestCase(TestCase):
    """
    Very basic tests around the app itself, not the code.
    """

    def test_no_pending_migrations(self):
        """
        Make sure all model changes are reflected with Django migrations.
        """
        output = StringIO()
        call_command(
            "makemigrations", "--dry-run", interactive=False, stdout=output
        )
        self.assertTrue("No changes detected" in output.getvalue())
