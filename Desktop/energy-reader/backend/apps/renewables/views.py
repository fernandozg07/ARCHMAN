from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from .models import RenewableProvider

class ProvidersView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Mock data for demo
        data = [{
            'id': 1,
            'name': 'Solar Energy Pro',
            'description': 'Especialista em energia solar',
            'rating': 4.8,
            'min_installation_kw': 2.0,
            'price_per_kw': 3500.00
        }]
        
        return Response({'providers': data})

class QuoteRequestView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Simulação de solicitação de orçamento
        provider_id = request.data.get('provider_id')
        consumption = request.data.get('consumption', 0)
        
        if not provider_id:
            return Response({'error': 'Provider ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': 'Solicitação enviada com sucesso',
            'estimated_savings': consumption * 0.3,  # 30% economia estimada
            'contact_time': '24-48 horas'
        })