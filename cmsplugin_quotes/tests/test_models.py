from django.test import TestCase
from quotes.models import Quote


class QuoteTestCase(TestCase):

    def test_create(self):
        ts = Quote(author="A", text="ABC")
        ts.save()
        self.assertEqual(str(ts), "A ABC")