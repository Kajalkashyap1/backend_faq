import pytest
from unittest.mock import patch
from django.db import IntegrityError
from .models import FAQ  # Update with the actual path to your model

@pytest.mark.django_db
class TestFAQModel:
    
    @patch('googletrans.Translator.translate')
    def test_faq_save_translation(self, mock_translate):
        # Mock the translated text returned by the Google Translator
        mock_translate.return_value.text = "Translated Question"
        
        # Create an FAQ instance
        faq = FAQ.objects.create(
            question="This is a test question",
            answer="This is a test answer",
            language="hi",  # Translate to Hindi
        )
        
        # Save the instance
        faq.save()

        # Check if the translation is applied correctly
        assert faq.question == "Translated Question"
        assert faq.answer == "Translated Question"  # As the same mock is used for both fields

    @patch('googletrans.Translator.translate')
    def test_faq_save_answer_translation(self, mock_translate):
        # Mock the translated text returned by the Google Translator
        mock_translate.side_effect = [
            # First translation for the question
            mock_translate.return_value._replace(text="Translated Question"),
            # Second translation for the answer
            mock_translate.return_value._replace(text="Translated Answer"),
        ]

        # Create an FAQ instance
        faq = FAQ.objects.create(
            question="This is a test question",
            answer="This is a test answer",
            language="bn",  # Translate to Bengali
        )

        # Save the instance
        faq.save()

        # Check if both question and answer translations are applied correctly
        assert faq.question == "Translated Question"
        assert faq.answer == "Translated Answer"

    def test_faq_save_without_answer(self):
        # Test when there is no answer to translate
        faq = FAQ.objects.create(
            question="This is a test question",
            answer="",
            language="hi",  # Translate to Hindi
        )
        
        # Save the instance
        faq.save()
        
        # The question should be translated, but answer should remain empty
        assert faq.question != "This is a test question"
        assert faq.answer == ""  # Answer should remain empty
