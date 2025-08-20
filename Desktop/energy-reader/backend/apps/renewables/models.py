from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

User = get_user_model()


class Provider(models.Model):
    """Renewable energy provider"""
    
    class ModalityType(models.TextChoices):
        SOLAR_TELHADO = 'SOLAR_TELHADO', 'Solar Telhado'
        SOLAR_FAZENDA = 'SOLAR_FAZENDA', 'Solar Fazenda'
        EOLICA = 'EOLICA', 'Eólica'
        GC = 'GC', 'Geração Compartilhada'
        REC = 'REC', 'REC'
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    site = models.URLField(blank=True)
    contato_email = models.EmailField(blank=True)
    contato_telefone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        blank=True
    )
    
    # Coverage areas
    cobertura_ufs = models.JSONField(
        default=list,
        help_text='Lista de UFs atendidas: ["SP", "RJ", "MG"]'
    )
    cobertura_ceps = models.JSONField(
        default=list,
        help_text='Faixas de CEP: [{"inicio": "01000", "fim": "05999"}]'
    )
    
    # Modalities offered
    modalidades = models.JSONField(
        default=list,
        help_text='Modalidades oferecidas'
    )
    
    # Business info
    cnpj = models.CharField(
        max_length=18,
        validators=[RegexValidator(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$')],
        blank=True
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'renewable_providers'
        verbose_name = 'Fornecedor de Energia Renovável'
        verbose_name_plural = 'Fornecedores de Energia Renovável'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    def covers_cep(self, cep: str) -> bool:
        """Check if provider covers given CEP"""
        # Remove formatting
        clean_cep = cep.replace('-', '').replace('.', '')
        
        for cep_range in self.cobertura_ceps:
            inicio = cep_range.get('inicio', '')
            fim = cep_range.get('fim', '')
            
            if inicio <= clean_cep <= fim:
                return True
        
        return False


class Offer(models.Model):
    """Renewable energy offer"""
    
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='offers')
    
    # Geographic coverage
    regiao = models.CharField(max_length=100, help_text='Região/Estado atendido')
    cep_mask = models.CharField(
        max_length=10,
        help_text='Máscara de CEP (ex: 01000-05999)',
        blank=True
    )
    
    # Pricing
    preco_estimado_kwh = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        validators=[MinValueValidator(0)],
        help_text='Preço estimado por kWh em R$'
    )
    economia_estimada_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Economia estimada em %'
    )
    
    # Service info
    modalidade = models.CharField(
        max_length=20,
        choices=Provider.ModalityType.choices,
        default=Provider.ModalityType.SOLAR_TELHADO
    )
    sla_contato_horas = models.IntegerField(
        default=24,
        validators=[MinValueValidator(1), MaxValueValidator(168)],
        help_text='SLA de contato em horas'
    )
    
    # Investment info
    investimento_minimo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Investimento mínimo em R$'
    )
    payback_meses = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(240)],
        help_text='Payback estimado em meses'
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'renewable_offers'
        verbose_name = 'Oferta de Energia Renovável'
        verbose_name_plural = 'Ofertas de Energia Renovável'
        ordering = ['economia_estimada_percent']
        indexes = [
            models.Index(fields=['regiao', 'is_active']),
            models.Index(fields=['modalidade', 'is_active']),
        ]
    
    def __str__(self):
        return f'{self.provider.nome} - {self.regiao} - {self.economia_estimada_percent}%'


class Lead(models.Model):
    """Lead generated from renewable energy interest"""
    
    class Status(models.TextChoices):
        NEW = 'NEW', 'Novo'
        CONTACTED = 'CONTACTED', 'Contatado'
        QUALIFIED = 'QUALIFIED', 'Qualificado'
        PROPOSAL_SENT = 'PROPOSAL_SENT', 'Proposta Enviada'
        CLOSED_WON = 'CLOSED_WON', 'Fechado - Ganho'
        CLOSED_LOST = 'CLOSED_LOST', 'Fechado - Perdido'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='renewable_leads')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='leads')
    
    # Lead info
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    consumo_medio_kwh = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Consumo médio mensal em kWh'
    )
    custo_medio_mensal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Custo médio mensal em R$'
    )
    
    # Contact preferences
    melhor_horario_contato = models.CharField(max_length=50, blank=True)
    observacoes = models.TextField(blank=True)
    
    # LGPD consent
    consentimento_lgpd = models.BooleanField(
        default=False,
        help_text='Consentimento para compartilhamento de dados'
    )
    consentimento_data = models.DateTimeField(null=True, blank=True)
    
    # Provider interaction
    contatado_em = models.DateTimeField(null=True, blank=True)
    proposta_enviada_em = models.DateTimeField(null=True, blank=True)
    fechado_em = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'renewable_leads'
        verbose_name = 'Lead de Energia Renovável'
        verbose_name_plural = 'Leads de Energia Renovável'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['offer', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f'Lead {self.id} - {self.user.email} - {self.offer.provider.nome}'