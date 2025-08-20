import logging
from celery import shared_task
from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import datetime
from decimal import Decimal
from apps.billing.models import Bill
from .models import MetricSnapshot, ConsumptionTrend

logger = logging.getLogger(__name__)


@shared_task
def create_metric_snapshot_task(bill_id):
    """Create metric snapshot for a processed bill"""
    try:
        bill = Bill.objects.get(id=bill_id, status=Bill.Status.PROCESSED)
        
        # Create or update metric snapshot
        snapshot, created = MetricSnapshot.objects.get_or_create(
            bill=bill,
            defaults={
                'user': bill.user,
                'kwh_consumed': bill.consumo_kwh,
                'kwh_cost': bill.tarifa_kwh,
                'eficiencia_score': _calculate_efficiency_score(bill)
            }
        )
        
        if not created:
            # Update existing snapshot
            snapshot.kwh_consumed = bill.consumo_kwh
            snapshot.kwh_cost = bill.tarifa_kwh
            snapshot.eficiencia_score = _calculate_efficiency_score(bill)
            snapshot.save()
        
        # Update consumption trends
        _update_consumption_trends(bill)
        
        logger.info("Created metric snapshot")
        
    except Bill.DoesNotExist:
        logger.error("Bill not found or not processed")
    except Exception as exc:
        logger.error(f"Error creating metric snapshot: {type(exc).__name__}")


@shared_task
def update_all_trends_task():
    """Update consumption trends for all users (run monthly)"""
    try:
        # Get all users with processed bills
        users_with_bills = Bill.objects.filter(
            status=Bill.Status.PROCESSED
        ).values_list('user_id', flat=True).distinct()
        
        for user_id in users_with_bills:
            _update_user_trends(user_id)
        
        logger.info(f"Updated trends for {len(users_with_bills)} users")
        
    except Exception as exc:
        logger.error(f"Error updating trends: {type(exc).__name__}")


def _calculate_efficiency_score(bill):
    """Calculate efficiency score for a bill"""
    if not bill.tarifa_kwh:
        return None
    
    # Compare with national average (example: R$ 0.65/kWh)
    national_avg = Decimal('0.65')
    
    if bill.tarifa_kwh <= national_avg * Decimal('0.8'):
        return Decimal('9.0')  # Very efficient
    elif bill.tarifa_kwh <= national_avg:
        return Decimal('7.0')  # Good
    elif bill.tarifa_kwh <= national_avg * Decimal('1.2'):
        return Decimal('5.0')  # Average
    else:
        return Decimal('3.0')  # Needs improvement


def _update_consumption_trends(bill):
    """Update consumption trends for bill's period"""
    if not bill.period_start:
        return
    
    year = bill.period_start.year
    month = bill.period_start.month
    
    # Get all bills for this user in the same month/year
    monthly_bills = Bill.objects.filter(
        user=bill.user,
        status=Bill.Status.PROCESSED,
        period_start__year=year,
        period_start__month=month
    )
    
    # Calculate aggregated metrics
    total_kwh = monthly_bills.aggregate(Sum('consumo_kwh'))['consumo_kwh__sum'] or 0
    total_cost = monthly_bills.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    avg_cost_per_kwh = monthly_bills.aggregate(Avg('tarifa_kwh'))['tarifa_kwh__avg'] or 0
    
    # Calculate daily average (assuming 30 days)
    avg_daily_kwh = total_kwh / 30 if total_kwh else 0
    
    # Get previous month for comparison
    previous_trend = ConsumptionTrend.objects.filter(
        user=bill.user,
        year=year if month > 1 else year - 1,
        month=month - 1 if month > 1 else 12
    ).first()
    
    kwh_change_percent = None
    cost_change_percent = None
    
    if previous_trend:
        if previous_trend.total_kwh > 0:
            kwh_change_percent = ((total_kwh - previous_trend.total_kwh) / previous_trend.total_kwh) * 100
        if previous_trend.total_cost > 0:
            cost_change_percent = ((total_cost - previous_trend.total_cost) / previous_trend.total_cost) * 100
    
    # Check for anomalies (simple threshold-based)
    is_anomaly = False
    anomaly_reason = ""
    
    if previous_trend:
        if kwh_change_percent and abs(kwh_change_percent) > 50:
            is_anomaly = True
            anomaly_reason = f"Variação de {kwh_change_percent:.1f}% no consumo"
    
    # Create or update trend
    trend, created = ConsumptionTrend.objects.update_or_create(
        user=bill.user,
        year=year,
        month=month,
        defaults={
            'total_kwh': total_kwh,
            'total_cost': total_cost,
            'avg_daily_kwh': avg_daily_kwh,
            'avg_cost_per_kwh': avg_cost_per_kwh,
            'kwh_change_percent': kwh_change_percent,
            'cost_change_percent': cost_change_percent,
            'is_anomaly': is_anomaly,
            'anomaly_reason': anomaly_reason
        }
    )
    
    logger.info(f"Updated trend for {bill.user.email} - {month}/{year}")


def _update_user_trends(user_id):
    """Update all trends for a specific user"""
    try:
        bills = Bill.objects.filter(
            user_id=user_id,
            status=Bill.Status.PROCESSED
        ).order_by('period_start')
        
        for bill in bills:
            _update_consumption_trends(bill)
            
    except Exception as exc:
        logger.error(f"Error updating trends for user: {type(exc).__name__}")