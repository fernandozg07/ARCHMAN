import html
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class AuditEvent(models.Model):
    """Audit log for system events"""
    
    class Action(models.TextChoices):
        CREATE = 'CREATE', 'Criar'
        READ = 'READ', 'Ler'
        UPDATE = 'UPDATE', 'Atualizar'
        DELETE = 'DELETE', 'Deletar'
        LOGIN = 'LOGIN', 'Login'
        LOGOUT = 'LOGOUT', 'Logout'
        UPLOAD = 'UPLOAD', 'Upload'
        PROCESS = 'PROCESS', 'Processar'
        EXPORT = 'EXPORT', 'Exportar'
        ADMIN_ACTION = 'ADMIN_ACTION', 'Ação Admin'
    
    # Actor (who performed the action)
    actor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='audit_events'
    )
    actor_email = models.EmailField(blank=True)  # Store email in case user is deleted
    
    # Action details
    action = models.CharField(max_length=20, choices=Action.choices)
    resource = models.CharField(max_length=100, help_text='Resource type (e.g., Bill, User)')
    resource_id = models.CharField(max_length=50, blank=True)
    
    # Generic foreign key to the affected object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Request details
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Additional data
    payload = models.JSONField(default=dict, blank=True)
    description = models.TextField(blank=True)
    
    # Result
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_events'
        verbose_name = 'Evento de Auditoria'
        verbose_name_plural = 'Eventos de Auditoria'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['actor', 'created_at']),
            models.Index(fields=['action', 'created_at']),
            models.Index(fields=['resource', 'created_at']),
            models.Index(fields=['ip_address', 'created_at']),
        ]
    
    def __str__(self):
        actor_name = self.actor_email or (self.actor.email if self.actor else 'Sistema')
        return f'{html.escape(actor_name)} - {self.action} - {html.escape(self.resource)} - {self.created_at}'
    
    def save(self, *args, **kwargs):
        # Store actor email for reference
        if self.actor and not self.actor_email:
            self.actor_email = self.actor.email
        super().save(*args, **kwargs)


class LoginAttempt(models.Model):
    """Track login attempts for security monitoring"""
    
    class Status(models.TextChoices):
        SUCCESS = 'SUCCESS', 'Sucesso'
        FAILED = 'FAILED', 'Falhou'
        BLOCKED = 'BLOCKED', 'Bloqueado'
    
    email = models.EmailField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices)
    failure_reason = models.CharField(max_length=100, blank=True)
    
    # Geolocation (optional)
    country = models.CharField(max_length=2, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'login_attempts'
        verbose_name = 'Tentativa de Login'
        verbose_name_plural = 'Tentativas de Login'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email', 'created_at']),
            models.Index(fields=['ip_address', 'created_at']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f'{html.escape(self.email)} - {self.status} - {self.ip_address} - {self.created_at}'


class DataExport(models.Model):
    """Track data exports for compliance"""
    
    class Format(models.TextChoices):
        CSV = 'CSV', 'CSV'
        EXCEL = 'EXCEL', 'Excel'
        JSON = 'JSON', 'JSON'
        PDF = 'PDF', 'PDF'
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendente'
        PROCESSING = 'PROCESSING', 'Processando'
        COMPLETED = 'COMPLETED', 'Concluído'
        FAILED = 'FAILED', 'Falhou'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exports')
    
    # Export details
    resource_type = models.CharField(max_length=50)
    format = models.CharField(max_length=10, choices=Format.choices)
    filters = models.JSONField(default=dict, blank=True)
    
    # File info
    filename = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    records_count = models.PositiveIntegerField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    error_message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'data_exports'
        verbose_name = 'Exportação de Dados'
        verbose_name_plural = 'Exportações de Dados'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f'{html.escape(self.user.email)} - {html.escape(self.resource_type)} - {self.format} - {self.status}'