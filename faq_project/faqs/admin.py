from django.contrib import admin
from django.utils.html import format_html
from .models import FAQ

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_short', 'formatted_answer', 'created_at', 'updated_at')  # ❌ Removed 'language'
    search_fields = ('question', 'answer')
    ordering = ('-created_at',)

    def question_short(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_short.short_description = "Question"

    def formatted_answer(self, obj):
        return format_html(f"<div style='max-width: 300px; overflow: hidden;'>{obj.answer[:100]}...</div>")
    formatted_answer.short_description = "Answer Preview"

admin.site.register(FAQ, FAQAdmin)
