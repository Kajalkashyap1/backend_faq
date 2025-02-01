from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from googletrans import Translator
from .models import FAQ
from .serializers import FAQSerializer

# 🟢 Fetch FAQs with language filtering
@api_view(['GET'])
def get_faqs(request):
    lang = request.GET.get('lang', 'en')
    cache_key = f"faqs_{lang}"
    faqs = cache.get(cache_key)

    if not faqs:
        faqs = FAQ.objects.filter(language=lang)
        serializer = FAQSerializer(faqs, many=True)
        cache.set(cache_key, serializer.data, timeout=3600)  # Cache for 1 hour
    else:
        serializer = FAQSerializer(faqs, many=True)
    
    return Response(serializer.data)

# 🟢 Update an existing FAQ
@api_view(['PUT'])
def update_faq(request, id):
    try:
        faq = FAQ.objects.get(id=id)
    except FAQ.DoesNotExist:
        return Response({"error": "FAQ not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = FAQSerializer(faq, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🟢 Delete an FAQ
@api_view(['DELETE'])
def delete_faq(request, id):
    try:
        faq = FAQ.objects.get(id=id)
    except FAQ.DoesNotExist:
        return Response({"error": "FAQ not found"}, status=status.HTTP_404_NOT_FOUND)

    faq.delete()
    return Response({"message": "FAQ deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
