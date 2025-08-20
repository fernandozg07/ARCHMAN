from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg
from apps.billing.models import Bill

class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bills = Bill.objects.filter(user=request.user, status='PROCESSED')
        all_bills = Bill.objects.filter(user=request.user)
        
        total_bills = bills.count()
        total_value = bills.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        total_consumption = bills.aggregate(Sum('consumo_kwh'))['consumo_kwh__sum'] or 0
        avg_value = bills.aggregate(Avg('valor_total'))['valor_total__avg'] or 0
        avg_consumption = bills.aggregate(Avg('consumo_kwh'))['consumo_kwh__avg'] or 0
        
        # Status breakdown
        status_counts = {
            'processed': all_bills.filter(status='PROCESSED').count(),
            'processing': all_bills.filter(status='PROCESSING').count(),
            'failed': all_bills.filter(status='FAILED').count(),
            'uploaded': all_bills.filter(status='UPLOADED').count(),
        }
        
        # Monthly data (last 6 months)
        from datetime import datetime, timedelta
        monthly_data = []
        for i in range(6):
            month_start = datetime.now().replace(day=1) - timedelta(days=30*i)
            month_bills = bills.filter(created_at__month=month_start.month, created_at__year=month_start.year)
            monthly_data.append({
                'month': month_start.strftime('%b'),
                'bills': month_bills.count(),
                'value': float(month_bills.aggregate(Sum('valor_total'))['valor_total__sum'] or 0),
                'consumption': float(month_bills.aggregate(Sum('consumo_kwh'))['consumo_kwh__sum'] or 0)
            })
        
        return Response({
            'total_bills': total_bills,
            'total_value': f"{total_value:.2f}",
            'total_consumption': f"{total_consumption:.2f}",
            'average_value': f"{avg_value:.2f}",
            'average_consumption': f"{avg_consumption:.2f}",
            'status_counts': status_counts,
            'monthly_data': list(reversed(monthly_data)),
            'last_bill': bills.order_by('-created_at').first().created_at.isoformat() if bills.exists() else None
        })

class TrendsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'trends': [],
            'message': 'Trends analysis coming soon'
        })