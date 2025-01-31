from django.db import models
from ckeditor.fields import RichTextField

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()  # WYSIWYG editor support
    language = models.CharField(max_length=5, choices=[('en', 'English'), ('hi', 'Hindi'), ('bn', 'Bengali')])

    def __str__(self):
        return self.question
