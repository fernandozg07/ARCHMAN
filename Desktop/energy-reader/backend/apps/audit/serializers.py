from rest_framework import serializers
from .models import AuditEvent, LoginAttempt, DataExport


class AuditEventSerializer(serializers.ModelSerializer):
    """Serializer for audit events"""
    actor_email = serializers.EmailField(read_only=True)
    
    class Meta:
        model = AuditEvent
        fields = [
            'id', 'actor_email', 'action', 'resource', 'resource_id',
            'ip_address', 'description', 'success', 'error_message',
            'created_at'
        ]


class LoginAttemptSerializer(serializers.ModelSerializer):
    """Serializer for login attempts"""
    
    class Meta:
        model = LoginAttempt
        fields = [
            'id', 'email', 'ip_address', 'status', 'failure_reason',
            'country', 'city', 'created_at'
        ]


class DataExportSerializer(serializers.ModelSerializer):
    """Serializer for data exports"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = DataExport
        fields = [
            'id', 'user_email', 'resource_type', 'format', 'filename',
            'file_size', 'records_count', 'status', 'error_message',
            'created_at', 'completed_at'
        ]


class AuditSummarySerializer(serializers.Serializer):
    """Serializer for audit summary statistics"""
    total_events = serializers.IntegerField()
    events_by_action = serializers.DictField()
    events_by_resource = serializers.DictField()
    failed_events = serializers.IntegerField()
    unique_users = serializers.IntegerField()
    login_attempts = serializers.IntegerField()
    failed_logins = serializers.IntegerField()
    exports_count = serializers.IntegerField()