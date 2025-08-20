from rest_framework import serializers
from .models import MetricSnapshot, ConsumptionTrend


class MetricSnapshotSerializer(serializers.ModelSerializer):
    """Serializer for metric snapshots"""
    
    class Meta:
        model = MetricSnapshot
        fields = [
            'id', 'bill', 'kwh_consumed', 'kwh_cost',
            'demanda_ponta', 'demanda_fora_ponta', 'pico_hora',
            'variacao_mensal_percent', 'eficiencia_score',
            'created_at', 'updated_at'
        ]


class ConsumptionTrendSerializer(serializers.ModelSerializer):
    """Serializer for consumption trends"""
    
    class Meta:
        model = ConsumptionTrend
        fields = [
            'id', 'year', 'month', 'total_kwh', 'total_cost',
            'avg_daily_kwh', 'avg_cost_per_kwh',
            'kwh_change_percent', 'cost_change_percent',
            'is_anomaly', 'anomaly_reason', 'created_at'
        ]


class AnalyticsSummarySerializer(serializers.Serializer):
    """Serializer for analytics summary"""
    
    # Current period
    current_kwh = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    current_cost = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    current_avg_kwh_cost = serializers.DecimalField(max_digits=8, decimal_places=4, allow_null=True)
    
    # Comparisons
    kwh_change_percent = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    cost_change_percent = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    
    # Projections
    projected_monthly_kwh = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    projected_monthly_cost = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    
    # Efficiency
    efficiency_score = serializers.DecimalField(max_digits=3, decimal_places=1, allow_null=True)
    potential_savings = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    
    # Trends
    trends = ConsumptionTrendSerializer(many=True)
    
    # Anomalies
    anomalies_count = serializers.IntegerField()
    last_anomaly = serializers.DateTimeField(allow_null=True)


class AnomalySerializer(serializers.Serializer):
    """Serializer for anomaly detection results"""
    
    period = serializers.CharField()
    kwh = serializers.DecimalField(max_digits=10, decimal_places=2)
    cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    z_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    is_anomaly = serializers.BooleanField()
    reason = serializers.CharField()


class ForecastSerializer(serializers.Serializer):
    """Serializer for consumption forecast"""
    
    period = serializers.CharField()
    predicted_kwh = serializers.DecimalField(max_digits=10, decimal_places=2)
    predicted_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    confidence_interval_low = serializers.DecimalField(max_digits=10, decimal_places=2)
    confidence_interval_high = serializers.DecimalField(max_digits=10, decimal_places=2)