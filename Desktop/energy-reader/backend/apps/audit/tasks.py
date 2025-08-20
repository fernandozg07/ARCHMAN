import csv
import logging
from io import StringIO
from celery import shared_task
from django.utils import timezone
from django.core.files.base import ContentFile
from .models import AuditEvent, DataExport

logger = logging.getLogger(__name__)


@shared_task
def export_audit_data_task(export_id):
    """Export audit data to CSV"""
    try:
        export_record = DataExport.objects.get(id=export_id)
        export_record.status = DataExport.Status.PROCESSING
        export_record.save()
        
        # Get audit events based on filters
        queryset = AuditEvent.objects.all().order_by('-created_at')
        
        filters = export_record.filters
        if filters.get('start_date'):
            queryset = queryset.filter(created_at__gte=filters['start_date'])
        if filters.get('end_date'):
            queryset = queryset.filter(created_at__lte=filters['end_date'])
        if filters.get('action'):
            queryset = queryset.filter(action=filters['action'])
        if filters.get('resource'):
            queryset = queryset.filter(resource=filters['resource'])
        
        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'ID', 'Actor Email', 'Action', 'Resource', 'Resource ID',
            'IP Address', 'User Agent', 'Success', 'Error Message',
            'Description', 'Created At'
        ])
        
        # Write data
        count = 0
        for event in queryset:
            writer.writerow([
                event.id,
                event.actor_email,
                event.action,
                event.resource,
                event.resource_id,
                event.ip_address,
                event.user_agent,
                'Yes' if event.success else 'No',
                event.error_message,
                event.description,
                event.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
            count += 1
        
        # Save file info
        csv_content = output.getvalue()
        filename = f'audit_export_{export_record.id}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        export_record.filename = filename
        export_record.file_size = len(csv_content.encode('utf-8'))
        export_record.records_count = count
        export_record.status = DataExport.Status.COMPLETED
        export_record.completed_at = timezone.now()
        export_record.save()
        
        logger.info(f"Exported {count} audit events to file")
        
        # In a real implementation, you would save the file to storage
        # and possibly send an email notification to the user
        
    except DataExport.DoesNotExist:
        logger.error("Export record not found")
    except Exception as exc:
        logger.error(f"Error exporting audit data: {type(exc).__name__}")
        
        try:
            export_record = DataExport.objects.get(id=export_id)
            export_record.status = DataExport.Status.FAILED
            export_record.error_message = str(exc)
            export_record.save()
        except DataExport.DoesNotExist:
            pass


@shared_task
def cleanup_old_audit_events():
    """Clean up old audit events (run weekly)"""
    try:
        # Keep audit events for 1 year
        cutoff_date = timezone.now() - timezone.timedelta(days=365)
        
        deleted_count = AuditEvent.objects.filter(
            created_at__lt=cutoff_date
        ).delete()[0]
        
        logger.info(f"Cleaned up {deleted_count} old audit events")
        
    except Exception as exc:
        logger.error(f"Error cleaning up audit events: {type(exc).__name__}")


@shared_task
def log_audit_event(actor_id, action, resource, **kwargs):
    """Log audit event asynchronously"""
    try:
        from apps.accounts.models import User
        
        actor = None
        if actor_id:
            try:
                actor = User.objects.get(id=actor_id)
            except User.DoesNotExist:
                pass
        
        AuditEvent.objects.create(
            actor=actor,
            action=action,
            resource=resource,
            **kwargs
        )
        
    except Exception as exc:
        logger.error(f"Error logging audit event: {type(exc).__name__}")