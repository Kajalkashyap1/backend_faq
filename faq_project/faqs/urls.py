from django.urls import path
from .views import get_faqs

urlpatterns = [
    path('api/faqs/', get_faqs, name='get_faqs'),
    # path('api/faqs/<int:id>/', update_faq, name='update_faq'),
    # path('api/faqs/<int:id>/', delete_faq, name='delete_faq'),
]
