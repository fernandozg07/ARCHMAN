from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import AuditEvent

class AuditEventListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        events = AuditEvent.objects.filter(actor=request.user).order_by('-created_at')[:50]
        
        data = [{
            'id': event.id,
            'action': event.action,
            'resource': event.resource,
            'success': event.success,
            'created_at': event.created_at
        } for event in events]
        
        return Response({'events': data})