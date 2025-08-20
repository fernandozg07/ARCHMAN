from django.contrib import admin
from django.utils.html import format_html
from .models import Bill


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """Admin for Bill model"""
    
    list_display = [
        'id', 'user_email', 'status', 'fornecedor', 'period_display',
        'consumo_kwh', 'valor_total', 'created_at'
    ]
    list_filter = [
        'status', 'fornecedor', 'bandeira_tarifaria', 
        'created_at', 'period_start'
    ]
    search_fields = [
        'user__email', 'numero_cliente', 'unidade_consumidora',
        'instalacao', 'file_hash'
    ]
    readonly_fields = [
        'file_hash', 'parsed_json', 'created_at', 'updated_at', 
        'processed_at', 'total_impostos', 'custo_kwh_efetivo'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'raw_file', 'file_hash', 'status', 'error_message')
        }),
        ('Dados Extraídos', {
            'fields': (
                'fornecedor', 'numero_cliente', 'unidade_consumidora', 
                'instalacao', 'endereco'
            )
        }),
        ('Período e Datas', {
            'fields': ('period_start', 'period_end', 'issue_date', 'due_date')
        }),
        ('Consumo e Valores', {
            'fields': (
                'consumo_kwh', 'tarifa_kwh', 'valor_total', 'bandeira_tarifaria',
                'total_impostos', 'custo_kwh_efetivo'
            )
        }),
        ('Impostos', {
            'fields': ('icms', 'pis', 'cofins', 'outros_impostos'),
            'classes': ('collapse',)
        }),
        ('Pagamento', {
            'fields': ('linha_digitavel', 'codigo_de_barras'),
            'classes': ('collapse',)
        }),
        ('Dados Brutos', {
            'fields': ('parsed_json',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'processed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email do Usuário'
    
    def period_display(self, obj):
        if obj.period_start and obj.period_end:
            return f"{obj.period_start} - {obj.period_end}"
        return "-"
    period_display.short_description = 'Período'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    actions = ['reprocess_bills']
    
    def reprocess_bills(self, request, queryset):
        """Action to reprocess selected bills"""
        from .tasks import process_bill_task
        
        count = 0
        for bill in queryset:
            bill.status = Bill.Status.UPLOADED
            bill.error_message = ''
            bill.save()
            process_bill_task.delay(bill.id)
            count += 1
        
        self.message_user(
            request, 
            f'{count} conta(s) enviada(s) para reprocessamento.'
        )
    
    reprocess_bills.short_description = 'Reprocessar contas selecionadas'