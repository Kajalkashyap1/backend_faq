import pytest
from django.contrib.admin.sites import site
from faqs.admin import FAQAdmin
from faqs.models import FAQ
from django.utils.html import escape

def test_faq_admin_registration():
    """Test that FAQ model is registered with the admin site."""
    assert FAQ in site._registry
    assert isinstance(site._registry[FAQ], FAQAdmin)

