import pytest
from django.urls import reverse, resolve
from faqs.views import get_faqs  

def test_faqs_url():
    """Test that the /api/faqs/ URL resolves correctly."""
    url = reverse('get_faqs')
    assert resolve(url).func == get_faqs
