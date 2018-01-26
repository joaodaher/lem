from django.core.management import call_command
from django.utils.six import StringIO
from v1.tests.tests_base import BaseApiTest


class MigrationTest(BaseApiTest):
    def test_missing_migration(self):
        out = StringIO()
        message = None
        try:
            call_command(
                'makemigrations',
                'v1',
                '--check',
                '--dry-run',
                interactive=False,
                stdout=out
            )
        except SystemExit:
            message = 'Missing migration. Run python manage.py makemigrations'
        self.assertIn('No changes', out.getvalue(), msg=message)
