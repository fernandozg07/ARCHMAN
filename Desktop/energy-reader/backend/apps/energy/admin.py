from django.contrib import admin
from .models import Distributor, Officer, Client, Quote, CommercialProposal, FinancialRecord

@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'region', 'active']
    list_filter = ['active', 'region']
    search_fields = ['name', 'code']

@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'city', 'is_active', 'created_at']
    list_filter = ['is_active', 'state', 'created_at']
    search_fields = ['full_name', 'email', 'cpf']
    filter_horizontal = ['distributors']
    
    fieldsets = (
        ('Dados da Empresa', {
            'fields': ('cnpj', 'cep', 'address', 'number', 'complement', 'neighborhood', 'city', 'state', 'distributors')
        }),
        ('Documentos', {
            'fields': ('contract_file', 'dcmi_file', 'id_document')
        }),
        ('Dados Pessoais', {
            'fields': ('full_name', 'cpf', 'rg', 'birth_date', 'email', 'phone', 'mother_name', 'father_name')
        }),
        ('Dados Bancários', {
            'fields': ('bank', 'agency', 'account', 'pix')
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'client_type', 'email', 'phone', 'city', 'status', 'officer', 'created_at']
    list_filter = ['client_type', 'status', 'state', 'created_at']
    search_fields = ['name', 'email', 'cpf_cnpj']
    
    fieldsets = (
        ('Dados Básicos', {
            'fields': ('name', 'cpf_cnpj', 'client_type', 'email', 'phone')
        }),
        ('Endereço', {
            'fields': ('address', 'neighborhood', 'city', 'state')
        }),
        ('Dados Pessoais', {
            'fields': ('birth_date', 'mother_name', 'father_name')
        }),
        ('Relacionamentos', {
            'fields': ('distributor', 'officer', 'status')
        })
    )

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'officer', 'installation_name', 'consumption_kwh', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['client__name', 'installation_name', 'installation_number']

@admin.register(CommercialProposal)
class CommercialProposalAdmin(admin.ModelAdmin):
    list_display = ['id', 'quote', 'generator_name', 'savings_percentage', 'is_best_proposal', 'accepted', 'created_at']
    list_filter = ['is_best_proposal', 'accepted', 'created_at']
    search_fields = ['generator_name', 'quote__client__name']

@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'officer', 'client', 'monthly_revenue', 'consolidated_remuneration', 'reference_month']
    list_filter = ['reference_month', 'created_at']
    search_fields = ['officer__full_name', 'client__name']