from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

from apps.accounts.models import User
from apps.energy.models import Officer, Client, Quote, FinancialRecord
from apps.accounts.serializers import UserSerializer
from apps.energy.serializers import OfficerSerializer, ClientSerializer

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        stats = {
            'total_users': User.objects.count(),
            'officers': User.objects.filter(user_type='officer').count(),
            'partners': User.objects.filter(user_type='partner').count(),
            'clients': User.objects.filter(user_type='client').count(),
            'new_users_this_month': User.objects.filter(
                created_at__gte=timezone.now().replace(day=1)
            ).count()
        }
        return Response(stats)

class AdminDashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        last_30_days = timezone.now() - timedelta(days=30)
        
        data = {
            'users': {
                'total': User.objects.count(),
                'new_this_month': User.objects.filter(created_at__gte=last_30_days).count(),
                'by_type': list(User.objects.values('user_type').annotate(count=Count('id')))
            },
            'officers': {
                'total': Officer.objects.count(),
                'active': Officer.objects.filter(is_active=True).count(),
                'pending': Officer.objects.filter(is_active=False).count()
            },
            'clients': {
                'total': Client.objects.count(),
                'active': Client.objects.filter(status='active').count(),
                'new_this_month': Client.objects.filter(created_at__gte=last_30_days).count()
            },
            'quotes': {
                'total': Quote.objects.count(),
                'pending': Quote.objects.filter(status='pending').count(),
                'completed': Quote.objects.filter(status='completed').count(),
                'this_month': Quote.objects.filter(created_at__gte=last_30_days).count()
            },
            'financial': {
                'total_revenue': FinancialRecord.objects.aggregate(
                    total=Sum('monthly_revenue')
                )['total'] or 0,
                'total_remuneration': FinancialRecord.objects.aggregate(
                    total=Sum('consolidated_remuneration')
                )['total'] or 0
            }
        }
        return Response(data)