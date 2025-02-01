from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator

class FAQ(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('bn', 'Bengali'),
    ]

    question = models.TextField()
    answer = RichTextField()  # WYSIWYG editor
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    created_at = models.DateTimeField(auto_now_add=True)  # New field
    updated_at = models.DateTimeField(auto_now=True)  # New field

    def save(self, *args, **kwargs):
        if self.language != 'en':  # Translate only non-English FAQs
            translator = Translator()
            self.question = translator.translate(self.question, src='en', dest=self.language).text
            self.answer = translator.translate(self.answer, src='en', dest=self.language).text
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.question[:50]} ({self.language})"  # Show first 50 chars and language
