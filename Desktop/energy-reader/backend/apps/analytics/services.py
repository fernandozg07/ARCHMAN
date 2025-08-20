import numpy as np
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from typing import Dict, List, Any
from apps.billing.models import Bill
from .models import MetricSnapshot, ConsumptionTrend


class AnalyticsService:
    """Service for analytics calculations"""
    
    def __init__(self, user):
        self.user = user
    
    def get_summary(self, window: str = '3m') -> Dict[str, Any]:
        """Get analytics summary for specified window"""
        months = self._parse_window(window)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=months * 30)
        
        # Get bills in period
        bills = Bill.objects.filter(
            user=self.user,
            status=Bill.Status.PROCESSED,
            period_start__gte=start_date,
            period_end__lte=end_date
        ).order_by('period_start')
        
        if not bills.exists():
            return self._empty_summary()
        
        # Current period metrics
        current_kwh = bills.aggregate(Sum('consumo_kwh'))['consumo_kwh__sum'] or 0
        current_cost = bills.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        current_avg_kwh_cost = bills.aggregate(Avg('tarifa_kwh'))['tarifa_kwh__avg']
        
        # Get trends
        trends = self._get_trends(months)
        
        # Calculate changes
        kwh_change, cost_change = self._calculate_changes(trends)
        
        # Projections
        projected_kwh, projected_cost = self._calculate_projections(bills)
        
        # Efficiency and savings
        efficiency_score = self._calculate_efficiency_score(bills)
        potential_savings = self._calculate_potential_savings(bills)
        
        # Anomalies
        anomalies = self.detect_anomalies()
        anomalies_count = len([a for a in anomalies if a['is_anomaly']])
        last_anomaly = max([a['period'] for a in anomalies if a['is_anomaly']], default=None)
        
        return {
            'current_kwh': current_kwh,
            'current_cost': current_cost,
            'current_avg_kwh_cost': current_avg_kwh_cost,
            'kwh_change_percent': kwh_change,
            'cost_change_percent': cost_change,
            'projected_monthly_kwh': projected_kwh,
            'projected_monthly_cost': projected_cost,
            'efficiency_score': efficiency_score,
            'potential_savings': potential_savings,
            'trends': trends,
            'anomalies_count': anomalies_count,
            'last_anomaly': last_anomaly
        }
    
    def detect_anomalies(self, threshold: float = 2.0) -> List[Dict[str, Any]]:
        """Detect anomalies using z-score"""
        trends = ConsumptionTrend.objects.filter(user=self.user).order_by('year', 'month')
        
        if trends.count() < 3:
            return []
        
        # Calculate z-scores for kWh consumption
        kwh_values = [float(t.total_kwh) for t in trends]
        kwh_mean = np.mean(kwh_values)
        kwh_std = np.std(kwh_values)
        
        anomalies = []
        for i, trend in enumerate(trends):
            if kwh_std > 0:
                z_score = (float(trend.total_kwh) - kwh_mean) / kwh_std
                is_anomaly = abs(z_score) > threshold
                
                reason = ""
                if is_anomaly:
                    if z_score > threshold:
                        reason = "Consumo muito acima da média"
                    else:
                        reason = "Consumo muito abaixo da média"
                
                anomalies.append({
                    'period': f"{trend.month:02d}/{trend.year}",
                    'kwh': trend.total_kwh,
                    'cost': trend.total_cost,
                    'z_score': round(z_score, 2),
                    'is_anomaly': is_anomaly,
                    'reason': reason
                })
        
        return anomalies
    
    def forecast_consumption(self, periods: int = 3) -> List[Dict[str, Any]]:
        """Forecast consumption using moving average"""
        trends = ConsumptionTrend.objects.filter(
            user=self.user
        ).order_by('-year', '-month')[:6]  # Last 6 months
        
        if trends.count() < 3:
            return []
        
        # Calculate moving averages
        kwh_values = [float(t.total_kwh) for t in reversed(trends)]
        cost_values = [float(t.total_cost) for t in reversed(trends)]
        
        kwh_ma = np.mean(kwh_values[-3:])  # 3-month moving average
        cost_ma = np.mean(cost_values[-3:])
        
        # Calculate confidence intervals (simple approach)
        kwh_std = np.std(kwh_values)
        cost_std = np.std(cost_values)
        
        forecasts = []
        current_date = timezone.now().date()
        
        for i in range(1, periods + 1):
            future_date = current_date + timedelta(days=30 * i)
            period_str = f"{future_date.month:02d}/{future_date.year}"
            
            forecasts.append({
                'period': period_str,
                'predicted_kwh': round(kwh_ma, 2),
                'predicted_cost': round(cost_ma, 2),
                'confidence_interval_low': round(kwh_ma - kwh_std, 2),
                'confidence_interval_high': round(kwh_ma + kwh_std, 2)
            })
        
        return forecasts
    
    def _parse_window(self, window: str) -> int:
        """Parse window string to months"""
        window_map = {
            '3m': 3,
            '6m': 6,
            '12m': 12
        }
        return window_map.get(window, 3)
    
    def _empty_summary(self) -> Dict[str, Any]:
        """Return empty summary when no data"""
        return {
            'current_kwh': None,
            'current_cost': None,
            'current_avg_kwh_cost': None,
            'kwh_change_percent': None,
            'cost_change_percent': None,
            'projected_monthly_kwh': None,
            'projected_monthly_cost': None,
            'efficiency_score': None,
            'potential_savings': None,
            'trends': [],
            'anomalies_count': 0,
            'last_anomaly': None
        }
    
    def _get_trends(self, months: int) -> List[Dict[str, Any]]:
        """Get consumption trends"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=months * 30)
        
        trends = ConsumptionTrend.objects.filter(
            user=self.user,
            year__gte=start_date.year,
            month__gte=start_date.month if start_date.year == end_date.year else 1
        ).order_by('year', 'month')
        
        return [
            {
                'id': t.id,
                'year': t.year,
                'month': t.month,
                'total_kwh': t.total_kwh,
                'total_cost': t.total_cost,
                'avg_daily_kwh': t.avg_daily_kwh,
                'avg_cost_per_kwh': t.avg_cost_per_kwh,
                'kwh_change_percent': t.kwh_change_percent,
                'cost_change_percent': t.cost_change_percent,
                'is_anomaly': t.is_anomaly,
                'anomaly_reason': t.anomaly_reason,
                'created_at': t.created_at
            }
            for t in trends
        ]
    
    def _calculate_changes(self, trends: List[Dict]) -> tuple:
        """Calculate percentage changes"""
        if len(trends) < 2:
            return None, None
        
        current = trends[-1]
        previous = trends[-2]
        
        kwh_change = None
        cost_change = None
        
        if previous['total_kwh'] and previous['total_kwh'] > 0:
            kwh_change = ((current['total_kwh'] - previous['total_kwh']) / previous['total_kwh']) * 100
        
        if previous['total_cost'] and previous['total_cost'] > 0:
            cost_change = ((current['total_cost'] - previous['total_cost']) / previous['total_cost']) * 100
        
        return kwh_change, cost_change
    
    def _calculate_projections(self, bills) -> tuple:
        """Calculate monthly projections"""
        if not bills.exists():
            return None, None
        
        # Simple average of last 3 months
        recent_bills = bills.order_by('-period_start')[:3]
        
        avg_kwh = recent_bills.aggregate(Avg('consumo_kwh'))['consumo_kwh__avg']
        avg_cost = recent_bills.aggregate(Avg('valor_total'))['valor_total__avg']
        
        return avg_kwh, avg_cost
    
    def _calculate_efficiency_score(self, bills) -> float:
        """Calculate efficiency score (0-10)"""
        if not bills.exists():
            return None
        
        # Simple efficiency based on cost per kWh compared to average
        user_avg_cost = bills.aggregate(Avg('tarifa_kwh'))['tarifa_kwh__avg']
        
        if not user_avg_cost:
            return None
        
        # Compare with national average (example: R$ 0.65/kWh)
        national_avg = Decimal('0.65')
        
        if user_avg_cost <= national_avg * Decimal('0.8'):
            return 9.0  # Very efficient
        elif user_avg_cost <= national_avg:
            return 7.0  # Good
        elif user_avg_cost <= national_avg * Decimal('1.2'):
            return 5.0  # Average
        else:
            return 3.0  # Needs improvement
    
    def _calculate_potential_savings(self, bills) -> float:
        """Calculate potential savings"""
        if not bills.exists():
            return None
        
        total_cost = bills.aggregate(Sum('valor_total'))['valor_total__sum']
        
        if not total_cost:
            return None
        
        # Estimate 10-15% savings with renewable energy
        return total_cost * Decimal('0.125')  # 12.5% average savings