import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.contenttypes.models import ContentType
from .models import AuditEvent


class AuditMiddleware(MiddlewareMixin):
    """Middleware to automatically log audit events"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        # Store request info for later use
        request._audit_data = {
            'ip_address': self._get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }
        return None
    
    def process_response(self, request, response):
        # Log certain API actions
        if hasattr(request, 'user') and request.user.is_authenticated:
            self._log_api_action(request, response)
        
        return response
    
    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _log_api_action(self, request, response):
        """Log API actions that should be audited"""
        # Only log certain methods and paths
        if request.method not in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return
        
        path = request.path_info
        
        # Skip non-API paths
        if not path.startswith('/api/'):
            return
        
        # Skip certain endpoints
        skip_paths = ['/api/auth/refresh/', '/api/me/']
        if any(path.startswith(skip_path) for skip_path in skip_paths):
            return
        
        # Determine action and resource
        action, resource = self._parse_action_resource(request.method, path)
        
        if not action or not resource:
            return
        
        # Get request data (be careful with sensitive data)
        payload = {}
        if hasattr(request, 'data') and request.data:
            payload = self._sanitize_payload(dict(request.data))
        
        # Create audit event
        try:
            AuditEvent.objects.create(
                actor=request.user,
                action=action,
                resource=resource,
                ip_address=request._audit_data.get('ip_address'),
                user_agent=request._audit_data.get('user_agent'),
                payload=payload,
                success=200 <= response.status_code < 400,
                error_message='' if 200 <= response.status_code < 400 else f'HTTP {response.status_code}'
            )
        except Exception:
            # Don't break the request if audit logging fails
            pass
    
    def _parse_action_resource(self, method, path):
        """Parse HTTP method and path to determine action and resource"""
        action_map = {
            'POST': AuditEvent.Action.CREATE,
            'PUT': AuditEvent.Action.UPDATE,
            'PATCH': AuditEvent.Action.UPDATE,
            'DELETE': AuditEvent.Action.DELETE,
        }
        
        action = action_map.get(method)
        
        # Extract resource from path
        resource = None
        if '/bills/' in path:
            if 'upload' in path:
                action = AuditEvent.Action.UPLOAD
            resource = 'Bill'
        elif '/renewables/' in path:
            if 'leads' in path:
                resource = 'Lead'
            else:
                resource = 'Renewable'
        elif '/auth/' in path:
            if 'login' in path:
                action = AuditEvent.Action.LOGIN
            resource = 'Auth'
        
        return action, resource
    
    def _sanitize_payload(self, payload):
        """Remove sensitive data from payload"""
        sensitive_fields = ['password', 'token', 'secret', 'key']
        
        sanitized = {}
        for key, value in payload.items():
            if any(sensitive in key.lower() for sensitive in sensitive_fields):
                sanitized[key] = '[REDACTED]'
            else:
                sanitized[key] = value
        
        return sanitized