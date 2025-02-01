import pytest
from faqs.serializers import FAQSerializer
from faqs.models import FAQ

def test_faq_serializer():
    """Test serialization of FAQ model."""
    faq_data = {"question": "What is Django?", "answer": "Django is a web framework."}
    serializer = FAQSerializer(data=faq_data)
    assert serializer.is_valid()
    assert serializer.validated_data == faq_data
