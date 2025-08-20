from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()

class Distributor(models.Model):
    """Distribuidoras de energia"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    region = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Officer(models.Model):
    """Cadastro de Officer"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Dados da Empresa
    cnpj = models.CharField(max_length=18)
    cep = models.CharField(max_length=9)
    address = models.CharField(max_length=200)
    number = models.CharField(max_length=10)
    complement = models.CharField(max_length=100, blank=True)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    distributors = models.ManyToManyField(Distributor, related_name='officers')
    
    # Documentos
    contract_file = models.FileField(upload_to='officers/contracts/', null=True, blank=True)
    dcmi_file = models.FileField(upload_to='officers/dcmi/', null=True, blank=True)
    
    # Dados Pessoais
    full_name = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=20)
    birth_date = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    mother_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    id_document = models.FileField(upload_to='officers/documents/', null=True, blank=True)
    
    # Dados Bancários
    bank = models.CharField(max_length=100)
    agency = models.CharField(max_length=10)
    account = models.CharField(max_length=20)
    pix = models.CharField(max_length=100)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.full_name

class Client(models.Model):
    """Cliente do sistema"""
    CLIENT_TYPES = [
        ('pf', 'Pessoa Física'),
        ('pj', 'Pessoa Jurídica'),
    ]
    
    # Dados básicos
    name = models.CharField(max_length=200)
    cpf_cnpj = models.CharField(max_length=18)
    client_type = models.CharField(max_length=2, choices=CLIENT_TYPES)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    # Endereço
    address = models.CharField(max_length=200)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    
    # Dados pessoais (para PF)
    birth_date = models.DateField(null=True, blank=True)
    mother_name = models.CharField(max_length=200, blank=True)
    father_name = models.CharField(max_length=200, blank=True)
    
    # Relacionamentos
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE, related_name='clients')
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('contracted', 'Contratado'),
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
    ], default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Quote(models.Model):
    """Cotação de energia"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='quotes')
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE)
    
    # Documentos
    energy_bill = models.FileField(upload_to='quotes/bills/', null=True, blank=True)
    negative_certificate = models.FileField(upload_to='quotes/certificates/', null=True, blank=True)
    
    # Dados da instalação
    installation_name = models.CharField(max_length=200)
    installation_number = models.CharField(max_length=50)
    consumption_kwh = models.DecimalField(max_digits=10, decimal_places=2)
    average_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('completed', 'Concluída'),
        ('expired', 'Expirada'),
    ], default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cotação {self.id} - {self.client.name}"

class CommercialProposal(models.Model):
    """Proposta Comercial"""
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='proposals')
    
    # Dados da geradora
    generator_name = models.CharField(max_length=200)
    
    # Proposta
    savings_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    estimated_rebate_12_months = models.DecimalField(max_digits=10, decimal_places=2)
    validity_term_days = models.IntegerField()
    prior_notice_days = models.IntegerField()
    contract_term_no_loyalty = models.BooleanField(default=True)
    co2_reduction = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    is_best_proposal = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Proposta {self.generator_name} - {self.savings_percentage}%"

class FinancialRecord(models.Model):
    """Registro Financeiro"""
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE, related_name='financial_records')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='financial_records')
    
    # Valores
    monthly_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    consolidated_remuneration = models.DecimalField(max_digits=12, decimal_places=2)
    contracted_discount = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Documentos
    invoice_file = models.FileField(upload_to='financial/invoices/', null=True, blank=True)
    
    # Data
    reference_month = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Financeiro {self.reference_month} - {self.officer.full_name}"
