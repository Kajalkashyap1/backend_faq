from django.urls import path
from .views import get_faqs, home



urlpatterns = [
     path('', home, name='home'),
    path('api/faqs/', get_faqs, name='get_faqs'),
]
