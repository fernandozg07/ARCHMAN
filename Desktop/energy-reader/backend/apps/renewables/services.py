import re
from decimal import Decimal
from django.db.models import Avg, Sum
from django.utils import timezone
from datetime import timedelta
from typing import Dict, List, Any
from apps.billing.models import Bill
from .models import Provider, Offer, Lead


class RenewableService:
    """Service for renewable energy calculations and matching"""
    
    def __init__(self, user):
        self.user = user
    
    def get_options_by_cep(self, cep: str, limit: int = 10) -> Dict[str, Any]:
        """Get renewable energy options for given CEP"""
        # Clean CEP
        clean_cep = re.sub(r'[^\d]', '', cep)
        
        if len(clean_cep) != 8:
            return {
                'cep': cep,
                'offers': [],
                'total_offers': 0,
                'consumo_medio_kwh': None,
                'custo_medio_mensal': None
            }
        
        # Get user's consumption data
        user_data = self._get_user_consumption_data()
        
        # Find matching offers
        offers = self._find_offers_by_cep(clean_cep, limit)
        
        # Calculate savings for each offer
        offers_with_savings = []
        for offer in offers:
            offer_data = self._calculate_offer_savings(offer, user_data)
            offers_with_savings.append(offer_data)
        
        # Sort by savings (descending)
        offers_with_savings.sort(
            key=lambda x: x.get('economia_anual_estimada', 0), 
            reverse=True
        )
        
        return {
            'cep': cep,
            'offers': offers_with_savings,
            'total_offers': len(offers_with_savings),
            'consumo_medio_kwh': user_data.get('consumo_medio_kwh'),
            'custo_medio_mensal': user_data.get('custo_medio_mensal')
        }
    
    def calculate_potential_savings(self) -> Dict[str, Any]:
        """Calculate potential savings with renewable energy"""
        user_data = self._get_user_consumption_data()
        
        if not user_data.get('custo_medio_mensal'):
            return {
                'error': 'Dados insuficientes para cálculo',
                'message': 'Faça upload de pelo menos uma conta para ver a economia potencial'
            }
        
        # Get best offers for user's CEP
        user_cep = self.user.cep
        if not user_cep:
            return {
                'error': 'CEP não informado',
                'message': 'Atualize seu perfil com o CEP para ver ofertas personalizadas'
            }
        
        options = self.get_options_by_cep(user_cep, 3)  # Top 3 offers
        
        if not options['offers']:
            return {
                'error': 'Nenhuma oferta disponível',
                'message': 'Não encontramos ofertas para sua região no momento'
            }
        
        best_offer = options['offers'][0]
        
        return {
            'consumo_medio_kwh': user_data['consumo_medio_kwh'],
            'custo_atual_mensal': user_data['custo_medio_mensal'],
            'custo_atual_anual': user_data['custo_medio_mensal'] * 12,
            'melhor_oferta': {
                'fornecedor': best_offer['provider']['nome'],
                'economia_percent': best_offer['economia_estimada_percent'],
                'economia_mensal': best_offer['economia_mensal_estimada'],
                'economia_anual': best_offer['economia_anual_estimada'],
                'payback_meses': best_offer.get('payback_meses'),
                'investimento_minimo': best_offer.get('investimento_minimo')
            },
            'total_ofertas': len(options['offers'])
        }
    
    def _get_user_consumption_data(self) -> Dict[str, Any]:
        """Get user's average consumption data from last 6 months"""
        six_months_ago = timezone.now().date() - timedelta(days=180)
        
        bills = Bill.objects.filter(
            user=self.user,
            status=Bill.Status.PROCESSED,
            period_start__gte=six_months_ago
        )
        
        if not bills.exists():
            return {}
        
        # Calculate averages
        avg_kwh = bills.aggregate(Avg('consumo_kwh'))['consumo_kwh__avg']
        avg_cost = bills.aggregate(Avg('valor_total'))['valor_total__avg']
        avg_tariff = bills.aggregate(Avg('tarifa_kwh'))['tarifa_kwh__avg']
        
        return {
            'consumo_medio_kwh': avg_kwh,
            'custo_medio_mensal': avg_cost,
            'tarifa_media_kwh': avg_tariff,
            'total_bills': bills.count()
        }
    
    def _find_offers_by_cep(self, cep: str, limit: int) -> List[Offer]:
        """Find offers that cover the given CEP"""
        # Get all active providers
        providers = Provider.objects.filter(is_active=True)
        
        matching_offers = []
        
        for provider in providers:
            if provider.covers_cep(cep):
                # Get active offers from this provider
                offers = provider.offers.filter(is_active=True)[:limit]
                matching_offers.extend(offers)
        
        # If no specific CEP matches, try by UF (first 2 digits)
        if not matching_offers:
            uf_code = cep[:2]
            # This is a simplified approach - in reality you'd have a CEP->UF mapping
            offers = Offer.objects.filter(
                provider__is_active=True,
                is_active=True,
                regiao__icontains=uf_code
            )[:limit]
            matching_offers.extend(offers)
        
        return matching_offers[:limit]
    
    def _calculate_offer_savings(self, offer: Offer, user_data: Dict) -> Dict[str, Any]:
        """Calculate savings for a specific offer"""
        # Base offer data
        offer_data = {
            'id': offer.id,
            'provider': {
                'id': offer.provider.id,
                'nome': offer.provider.nome,
                'descricao': offer.provider.descricao,
                'site': offer.provider.site,
                'contato_email': offer.provider.contato_email,
                'contato_telefone': offer.provider.contato_telefone,
                'modalidades': offer.provider.modalidades,
                'is_verified': offer.provider.is_verified
            },
            'regiao': offer.regiao,
            'modalidade': offer.modalidade,
            'preco_estimado_kwh': offer.preco_estimado_kwh,
            'economia_estimada_percent': offer.economia_estimada_percent,
            'sla_contato_horas': offer.sla_contato_horas,
            'investimento_minimo': offer.investimento_minimo,
            'payback_meses': offer.payback_meses,
            'economia_mensal_estimada': Decimal('0'),
            'economia_anual_estimada': Decimal('0')
        }
        
        # Calculate savings if user has consumption data
        custo_mensal = user_data.get('custo_medio_mensal')
        if custo_mensal:
            economia_decimal = offer.economia_estimada_percent / 100
            economia_mensal = custo_mensal * economia_decimal
            economia_anual = economia_mensal * 12
            
            offer_data.update({
                'economia_mensal_estimada': round(economia_mensal, 2),
                'economia_anual_estimada': round(economia_anual, 2)
            })
        
        return offer_data