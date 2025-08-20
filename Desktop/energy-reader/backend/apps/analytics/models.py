from django.db import models
from django.contrib.auth import get_user_model
from apps.billing.models import Bill

User = get_user_model()


class MetricSnapshot(models.Model):
    """Snapshot of metrics for analytics"""
    
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE, related_name='metrics')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metrics')
    
    # Consumption metrics
    kwh_consumed = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    kwh_cost = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    
    # Demand metrics (if available)
    demanda_ponta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    demanda_fora_ponta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Peak hour analysis
    pico_hora = models.CharField(max_length=20, blank=True)
    
    # Monthly variation
    variacao_mensal_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Efficiency metrics
    eficiencia_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'metric_snapshots'
        verbose_name = 'Snapshot de Métricas'
        verbose_name_plural = 'Snapshots de Métricas'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['bill']),
        ]
    
    def __str__(self):
        return f'Metrics {self.bill.id} - {self.user.email}'


class ConsumptionTrend(models.Model):
    """Consumption trends and patterns"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trends')
    
    # Period
    year = models.IntegerField()
    month = models.IntegerField()
    
    # Aggregated metrics
    total_kwh = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    avg_daily_kwh = models.DecimalField(max_digits=8, decimal_places=2)
    avg_cost_per_kwh = models.DecimalField(max_digits=8, decimal_places=4)
    
    # Comparison with previous period
    kwh_change_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    cost_change_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    # Flags
    is_anomaly = models.BooleanField(default=False)
    anomaly_reason = models.CharField(max_length=200, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'consumption_trends'
        verbose_name = 'Tendência de Consumo'
        verbose_name_plural = 'Tendências de Consumo'
        unique_together = ['user', 'year', 'month']
        ordering = ['-year', '-month']
        indexes = [
            models.Index(fields=['user', 'year', 'month']),
            models.Index(fields=['is_anomaly']),
        ]
    
    def __str__(self):
        return f'{self.user.email} - {self.month}/{self.year}'