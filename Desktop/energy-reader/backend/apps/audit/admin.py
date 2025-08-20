from django.contrib import admin
from django.utils.html import format_html
from .models import AuditEvent, LoginAttempt, DataExport


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    """Admin for AuditEvent model"""
    
    list_display = [
        'id', 'actor_email', 'action', 'resource', 'success_display',
        'ip_address', 'created_at'
    ]
    list_filter = ['action', 'resource', 'success', 'created_at']
    search_fields = ['actor_email', 'resource', 'ip_address', 'description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Ator', {
            'fields': ('actor', 'actor_email')
        }),
        ('Ação', {
            'fields': ('action', 'resource', 'resource_id', 'description')
        }),
        ('Contexto', {
            'fields': ('ip_address', 'user_agent', 'payload')
        }),
        ('Resultado', {
            'fields': ('success', 'error_message')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def success_display(self, obj):
        if obj.success:
            return format_html('<span style="color: green;">✓ Sucesso</span>')
        else:
            return format_html('<span style="color: red;">✗ Falha</span>')
    success_display.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False  # Don't allow manual creation
    
    def has_change_permission(self, request, obj=None):
        return False  # Don't allow editing
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superuser can delete


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    """Admin for LoginAttempt model"""
    
    list_display = [
        'email', 'status_display', 'ip_address', 'country', 'city', 'created_at'
    ]
    list_filter = ['status', 'country', 'created_at']
    search_fields = ['email', 'ip_address', 'city']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def status_display(self, obj):
        colors = {
            'SUCCESS': 'green',
            'FAILED': 'red',
            'BLOCKED': 'orange'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(DataExport)
class DataExportAdmin(admin.ModelAdmin):
    """Admin for DataExport model"""
    
    list_display = [
        'id', 'user_email', 'resource_type', 'format', 'status_display',
        'records_count', 'created_at'
    ]
    list_filter = ['resource_type', 'format', 'status', 'created_at']
    search_fields = ['user__email', 'filename']
    readonly_fields = ['created_at', 'completed_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Exportação', {
            'fields': ('resource_type', 'format', 'filters')
        }),
        ('Arquivo', {
            'fields': ('filename', 'file_size', 'records_count')
        }),
        ('Status', {
            'fields': ('status', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at')
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email do Usuário'
    
    def status_display(self, obj):
        colors = {
            'PENDING': 'orange',
            'PROCESSING': 'blue',
            'COMPLETED': 'green',
            'FAILED': 'red'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'