from django.contrib import admin
from django.utils.html import format_html
from .models import Provider, Offer, Lead


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    """Admin for Provider model"""
    
    list_display = [
        'nome', 'contato_email', 'is_active', 'is_verified', 
        'modalidades_display', 'created_at'
    ]
    list_filter = ['is_active', 'is_verified', 'created_at']
    search_fields = ['nome', 'contato_email', 'cnpj']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'cnpj')
        }),
        ('Contato', {
            'fields': ('site', 'contato_email', 'contato_telefone')
        }),
        ('Cobertura', {
            'fields': ('cobertura_ufs', 'cobertura_ceps')
        }),
        ('Serviços', {
            'fields': ('modalidades',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def modalidades_display(self, obj):
        return ', '.join(obj.modalidades) if obj.modalidades else '-'
    modalidades_display.short_description = 'Modalidades'


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """Admin for Offer model"""
    
    list_display = [
        'provider', 'regiao', 'modalidade', 'economia_estimada_percent',
        'preco_estimado_kwh', 'is_active', 'created_at'
    ]
    list_filter = ['modalidade', 'is_active', 'created_at', 'provider']
    search_fields = ['provider__nome', 'regiao']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('provider', 'regiao', 'cep_mask', 'modalidade')
        }),
        ('Preços e Economia', {
            'fields': (
                'preco_estimado_kwh', 'economia_estimada_percent',
                'investimento_minimo', 'payback_meses'
            )
        }),
        ('Atendimento', {
            'fields': ('sla_contato_horas',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """Admin for Lead model"""
    
    list_display = [
        'id', 'user_email', 'provider_name', 'status', 
        'consumo_medio_kwh', 'custo_medio_mensal', 'created_at'
    ]
    list_filter = ['status', 'consentimento_lgpd', 'created_at', 'offer__provider']
    search_fields = ['user__email', 'offer__provider__nome']
    readonly_fields = [
        'created_at', 'updated_at', 'consentimento_data',
        'contatado_em', 'proposta_enviada_em', 'fechado_em'
    ]
    
    fieldsets = (
        ('Informações do Lead', {
            'fields': ('user', 'offer', 'status')
        }),
        ('Dados de Consumo', {
            'fields': ('consumo_medio_kwh', 'custo_medio_mensal')
        }),
        ('Contato', {
            'fields': ('melhor_horario_contato', 'observacoes')
        }),
        ('LGPD', {
            'fields': ('consentimento_lgpd', 'consentimento_data')
        }),
        ('Histórico', {
            'fields': (
                'contatado_em', 'proposta_enviada_em', 'fechado_em'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email do Usuário'
    
    def provider_name(self, obj):
        return obj.offer.provider.nome
    provider_name.short_description = 'Fornecedor'
    
    actions = ['mark_as_contacted', 'mark_as_qualified']
    
    def mark_as_contacted(self, request, queryset):
        """Mark leads as contacted"""
        from django.utils import timezone
        
        count = queryset.update(
            status=Lead.Status.CONTACTED,
            contatado_em=timezone.now()
        )
        self.message_user(request, f'{count} lead(s) marcado(s) como contatado(s).')
    
    mark_as_contacted.short_description = 'Marcar como contatado'
    
    def mark_as_qualified(self, request, queryset):
        """Mark leads as qualified"""
        count = queryset.update(status=Lead.Status.QUALIFIED)
        self.message_user(request, f'{count} lead(s) marcado(s) como qualificado(s).')
    
    mark_as_qualified.short_description = 'Marcar como qualificado'