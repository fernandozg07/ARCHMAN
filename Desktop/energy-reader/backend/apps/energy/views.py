from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Distributor, Officer, Client, Quote, CommercialProposal, FinancialRecord
from .serializers import (
    DistributorSerializer, OfficerSerializer, ClientSerializer, 
    QuoteSerializer, CommercialProposalSerializer, FinancialRecordSerializer,
    DashboardStatsSerializer
)

class DistributorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Distributor.objects.filter(active=True)
    serializer_class = DistributorSerializer
    permission_classes = [IsAuthenticated]

class OfficerViewSet(viewsets.ModelViewSet):
    serializer_class = OfficerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Officer.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        officer = self.get_object()
        officer.is_active = not officer.is_active
        officer.save()
        return Response({'status': 'active' if officer.is_active else 'inactive'})

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            officer = Officer.objects.get(user=self.request.user)
            return Client.objects.filter(officer=officer)
        except Officer.DoesNotExist:
            return Client.objects.none()
    
    def perform_create(self, serializer):
        try:
            officer = Officer.objects.get(user=self.request.user)
            serializer.save(officer=officer)
        except Officer.DoesNotExist:
            return Response(
                {'error': 'Officer profile required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class QuoteViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            officer = Officer.objects.get(user=self.request.user)
            return Quote.objects.filter(officer=officer)
        except Officer.DoesNotExist:
            return Quote.objects.none()
    
    def perform_create(self, serializer):
        try:
            officer = Officer.objects.get(user=self.request.user)
            serializer.save(officer=officer)
        except Officer.DoesNotExist:
            return Response(
                {'error': 'Officer profile required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        quote = self.get_object()
        quote.status = 'processing'
        quote.save()
        
        # Criar propostas comerciais mock
        proposals_data = [
            {
                'generator_name': 'SolarTech Energia',
                'savings_percentage': 15.5,
                'estimated_rebate_12_months': 2400.00,
                'validity_term_days': 30,
                'prior_notice_days': 60,
                'co2_reduction': 1.2,
                'is_best_proposal': True
            },
            {
                'generator_name': 'EcoWind Power',
                'savings_percentage': 12.8,
                'estimated_rebate_12_months': 2100.00,
                'validity_term_days': 45,
                'prior_notice_days': 90,
                'co2_reduction': 1.0,
                'is_best_proposal': False
            }
        ]
        
        for proposal_data in proposals_data:
            CommercialProposal.objects.create(quote=quote, **proposal_data)
        
        quote.status = 'completed'
        quote.save()
        
        return Response({'status': 'processed', 'proposals_count': len(proposals_data)})

class CommercialProposalViewSet(viewsets.ModelViewSet):
    serializer_class = CommercialProposalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            officer = Officer.objects.get(user=self.request.user)
            return CommercialProposal.objects.filter(quote__officer=officer)
        except Officer.DoesNotExist:
            return CommercialProposal.objects.none()
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        proposal = self.get_object()
        proposal.accepted = True
        proposal.save()
        
        # Criar cliente se não existir
        quote = proposal.quote
        if quote.client.status == 'pending':
            quote.client.status = 'contracted'
            quote.client.save()
        
        return Response({'status': 'accepted'})

class FinancialRecordViewSet(viewsets.ModelViewSet):
    serializer_class = FinancialRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            officer = Officer.objects.get(user=self.request.user)
            return FinancialRecord.objects.filter(officer=officer)
        except Officer.DoesNotExist:
            return FinancialRecord.objects.none()
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        try:
            officer = Officer.objects.get(user=self.request.user)
            
            # Estatísticas do mês atual
            current_month = timezone.now().replace(day=1)
            
            stats = {
                'total_clients': officer.clients.filter(status='active').count(),
                'monthly_revenue': officer.financial_records.filter(
                    reference_month__gte=current_month
                ).aggregate(total=Sum('monthly_revenue'))['total'] or 0,
                'consolidated_remuneration': officer.financial_records.filter(
                    reference_month__gte=current_month
                ).aggregate(total=Sum('consolidated_remuneration'))['total'] or 0,
                'pending_quotes': officer.quote_set.filter(status='pending').count(),
                'active_proposals': CommercialProposal.objects.filter(
                    quote__officer=officer, 
                    accepted=False
                ).count()
            }
            
            serializer = DashboardStatsSerializer(stats)
            return Response(serializer.data)
            
        except Officer.DoesNotExist:
            return Response(
                {'error': 'Officer profile required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )