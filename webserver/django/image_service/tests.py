from django.test import TestCase
from io import StringIO
from django.core.management import call_command


class LoadTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('load', stdout=out)
        self.assertIn('Expected output', out.getvalue())
# Create your tests here.
