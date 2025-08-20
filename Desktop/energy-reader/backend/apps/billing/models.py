import hashlib
import os
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()


def bill_upload_path(instance, filename):
    """Generate upload path for bill files"""
    user_id = instance.user.id
    file_hash = hashlib.sha256(filename.encode()).hexdigest()[:16]
    return f'bills/{user_id}/{file_hash}_{filename}'


class Bill(models.Model):
    """Model for energy bills"""
    
    class Status(models.TextChoices):
        UPLOADED = 'UPLOADED', 'Enviado'
        PROCESSING = 'PROCESSING', 'Processando'
        PROCESSED = 'PROCESSED', 'Processado'
        FAILED = 'FAILED', 'Falhou'
    
    class BandeiraTarifaria(models.TextChoices):
        VERDE = 'VERDE', 'Verde'
        AMARELA = 'AMARELA', 'Amarela'
        VERMELHA = 'VERMELHA', 'Vermelha'
        ESCASSEZ_HIDRICA = 'ESCASSEZ_HIDRICA', 'Escassez Hídrica'
        DESCONHECIDA = 'DESCONHECIDA', 'Desconhecida'
    
    # Basic fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bills')
    raw_file = models.FileField(
        upload_to=bill_upload_path,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    file_hash = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADED)
    error_message = models.TextField(blank=True)
    
    # Parsed data (JSON schema)
    parsed_json = models.JSONField(null=True, blank=True)
    
    # Extracted fields (for easier querying)
    fornecedor = models.CharField(max_length=100, blank=True)
    numero_cliente = models.CharField(max_length=50, blank=True)
    unidade_consumidora = models.CharField(max_length=50, blank=True)
    instalacao = models.CharField(max_length=50, blank=True)
    endereco = models.TextField(blank=True)
    
    # Dates
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    
    # Values
    consumo_kwh = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tarifa_kwh = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bandeira_tarifaria = models.CharField(
        max_length=20, 
        choices=BandeiraTarifaria.choices, 
        default=BandeiraTarifaria.DESCONHECIDA
    )
    
    # Taxes
    icms = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pis = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cofins = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    outros_impostos = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Payment info
    linha_digitavel = models.CharField(max_length=48, blank=True)
    codigo_de_barras = models.CharField(max_length=44, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'bills'
        verbose_name = 'Conta de Energia'
        verbose_name_plural = 'Contas de Energia'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['period_start', 'period_end']),
            models.Index(fields=['file_hash']),
        ]
    
    def __str__(self):
        from django.utils.html import escape
        return escape(f'Conta {self.id} - {self.user.email} - {self.status}')
    
    def save(self, *args, **kwargs):
        if not self.file_hash and self.raw_file:
            # Generate file hash
            self.raw_file.seek(0)
            file_content = self.raw_file.read()
            self.file_hash = hashlib.sha256(file_content).hexdigest()
            self.raw_file.seek(0)
        super().save(*args, **kwargs)
    
    @property
    def total_impostos(self):
        """Calculate total taxes"""
        impostos = [self.icms, self.pis, self.cofins, self.outros_impostos]
        return sum(imposto for imposto in impostos if imposto is not None)
    
    @property
    def custo_kwh_efetivo(self):
        """Calculate effective cost per kWh including taxes"""
        if self.consumo_kwh and self.valor_total:
            return self.valor_total / self.consumo_kwh
        return None