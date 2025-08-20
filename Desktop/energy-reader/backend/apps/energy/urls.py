from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DistributorViewSet, OfficerViewSet, ClientViewSet, 
    QuoteViewSet, CommercialProposalViewSet, FinancialRecordViewSet
)

router = DefaultRouter()
router.register(r'distributors', DistributorViewSet)
router.register(r'officers', OfficerViewSet, basename='officer')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'quotes', QuoteViewSet, basename='quote')
router.register(r'proposals', CommercialProposalViewSet, basename='proposal')
router.register(r'financial', FinancialRecordViewSet, basename='financial')

urlpatterns = [
    path('', include(router.urls)),
]