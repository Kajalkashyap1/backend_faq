import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from faqs.models import FAQ
from faqs.serializers import FAQSerializer


@pytest.mark.django_db
class TestGetFaqsView:
    
    @pytest.fixture
    def create_faqs(self):
        # Fixture to create sample FAQs for testing
        FAQ.objects.create(question="Test question 1", answer="Test answer 1", language="en")
        FAQ.objects.create(question="Test question 2", answer="Test answer 2", language="en")
        FAQ.objects.create(question="Test question 3", answer="Test answer 3", language="hi")

    @pytest.fixture
    def client(self):
        # Fixture to initialize the APIClient
        return APIClient()

    @patch('django.core.cache.cache.get')
    @patch('django.core.cache.cache.set')
    @patch('faqs.views.FAQ.objects.filter')
    def test_get_faqs_from_cache(self, mock_filter, mock_cache_set, mock_cache_get, create_faqs, client):
        # Test if FAQs are fetched from cache
        mock_cache_get.return_value = [{"question": "Test question 1", "answer": "Test answer 1", "language": "en"}]
        
        response = client.get('/api/faqs/', {'lang': 'en'})
        
        # Ensure the response status is OK
        assert response.status_code == status.HTTP_200_OK
        
        # Ensure FAQs were fetched from cache
        mock_cache_get.assert_called_once_with("faqs_en")
        mock_cache_set.assert_not_called()  # Cache set should not be called if cache hit
        mock_filter.assert_not_called()  # Database query should not be called on cache hit
        
        # Ensure the response data matches the cached FAQ data
        assert response.data == [{"question": "Test question 1", "answer": "Test answer 1", "language": "en"}]

    