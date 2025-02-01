from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache
from deep_translator import GoogleTranslator
from .models import FAQ
from .serializers import FAQSerializer
from django.shortcuts import render


def home(request):
    return render(request, 'homepage.html') 

@api_view(['GET'])
def get_faqs(request):
    lang = request.GET.get('lang', 'en')  # Default to English
    cache_key = f"faqs_{lang}"

    # 🟢 Check if FAQs are cached
    faqs = cache.get(cache_key)

    if not faqs:
        faqs = FAQ.objects.all()  # ✅ Get all FAQs (no language filtering)

        translator = GoogleTranslator(source='auto', target=lang)  # Detect and translate any language
        translated_faqs = []

        for faq in faqs:
            translated_faq = {
                'question': translator.translate(faq.question),
                'answer': translator.translate(faq.answer),
            }
            translated_faqs.append(translated_faq)

        # ✅ Store in cache to reduce API calls
        cache.set(cache_key, translated_faqs, timeout=3600)  # Cache for 1 hour
        return Response(translated_faqs)

    return Response(faqs)  # Return cached FAQs
