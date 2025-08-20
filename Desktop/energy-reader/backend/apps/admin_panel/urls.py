from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminUserViewSet, AdminDashboardViewSet

router = DefaultRouter()
router.register(r'users', AdminUserViewSet)
router.register(r'dashboard', AdminDashboardViewSet, basename='admin-dashboard')

urlpatterns = [
    path('', include(router.urls)),
]