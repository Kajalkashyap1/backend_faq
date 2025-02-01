from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
import asyncio

class FAQ(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('bn', 'Bengali'),
    ]

    question = models.TextField()
    answer = RichTextField()  # WYSIWYG editor
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def save(self, *args, **kwargs):
        translator = Translator()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Translate question field
        translated_question = loop.run_until_complete(translator.translate(self.question, src='en', dest=self.language))
        self.question = translated_question.text  # Extract translated text properly
        
        # Translate answer field (if it exists)
        if self.answer:
            translated_answer = loop.run_until_complete(translator.translate(self.answer, src='en', dest=self.language))
            self.answer = translated_answer.text  # Extract translated text properly
        
        # Save the instance
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.question[:50]} ({self.language})"  # Show first 50 chars and language
