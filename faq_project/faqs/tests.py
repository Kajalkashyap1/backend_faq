from django.test import TestCase
from .models import FAQ

class FAQTestCase(TestCase):
    def setUp(self):
        FAQ.objects.create(question="What is Django?", answer="A Python framework.", language="en")

    def test_faq_creation(self):
        faq = FAQ.objects.get(language="en")
        self.assertEqual(faq.answer, "A Python framework.")
