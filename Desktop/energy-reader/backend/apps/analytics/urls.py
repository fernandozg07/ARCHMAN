from django.urls import path
from .views import AnalyticsView, TrendsView

urlpatterns = [
    path('summary/', AnalyticsView.as_view(), name='analytics-summary'),
    path('trends/', TrendsView.as_view(), name='analytics-trends'),
]