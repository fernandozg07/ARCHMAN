from django.contrib import admin
from .models import MetricSnapshot, ConsumptionTrend


@admin.register(MetricSnapshot)
class MetricSnapshotAdmin(admin.ModelAdmin):
    """Admin for MetricSnapshot model"""
    
    list_display = [
        'id', 'user_email', 'bill_id', 'kwh_consumed', 
        'kwh_cost', 'eficiencia_score', 'created_at'
    ]
    list_filter = ['created_at', 'eficiencia_score']
    search_fields = ['user__email', 'bill__id']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email do Usuário'
    
    def bill_id(self, obj):
        return obj.bill.id
    bill_id.short_description = 'ID da Conta'


@admin.register(ConsumptionTrend)
class ConsumptionTrendAdmin(admin.ModelAdmin):
    """Admin for ConsumptionTrend model"""
    
    list_display = [
        'id', 'user_email', 'period_display', 'total_kwh', 
        'total_cost', 'kwh_change_percent', 'is_anomaly'
    ]
    list_filter = ['year', 'month', 'is_anomaly', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-year', '-month']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email do Usuário'
    
    def period_display(self, obj):
        return f"{obj.month:02d}/{obj.year}"
    period_display.short_description = 'Período'