from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import FAQ
from .serializers import FAQSerializer
from django.core.cache import cache

@api_view(['GET'])
def get_faqs(request):
    lang = request.GET.get('lang', 'en') # default language is english
    cache_key = f"faqs_{lang}"
    faqs = cache.get(cache_key)

    if not faqs:
        faqs = FAQ.objects.filter(language=lang)
        serializer = FAQSerializer(faqs, many=True)
        cache.set(cache_key, serializer.data, timeout=60*60)  # Cache for 1 hour
    else:
        serializer = FAQSerializer(faqs, many=True)
    
    return Response(serializer.data)