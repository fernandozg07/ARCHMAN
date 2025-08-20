from django.urls import path
from .views import ProvidersView, QuoteRequestView

urlpatterns = [
    path('providers/', ProvidersView.as_view(), name='providers-list'),
    path('quote/', QuoteRequestView.as_view(), name='quote-request'),
]