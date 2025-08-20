from rest_framework import serializers
from django.utils import timezone
from .models import Provider, Offer, Lead


class ProviderSerializer(serializers.ModelSerializer):
    """Serializer for renewable energy providers"""
    
    class Meta:
        model = Provider
        fields = [
            'id', 'nome', 'descricao', 'site', 'contato_email', 
            'contato_telefone', 'modalidades', 'is_verified'
        ]


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for renewable energy offers"""
    provider = ProviderSerializer(read_only=True)
    
    class Meta:
        model = Offer
        fields = [
            'id', 'provider', 'regiao', 'modalidade',
            'preco_estimado_kwh', 'economia_estimada_percent',
            'sla_contato_horas', 'investimento_minimo', 'payback_meses'
        ]


class OfferWithSavingsSerializer(serializers.ModelSerializer):
    """Serializer for offers with calculated savings"""
    provider = ProviderSerializer(read_only=True)
    economia_mensal_estimada = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    economia_anual_estimada = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    
    class Meta:
        model = Offer
        fields = [
            'id', 'provider', 'regiao', 'modalidade',
            'preco_estimado_kwh', 'economia_estimada_percent',
            'sla_contato_horas', 'investimento_minimo', 'payback_meses',
            'economia_mensal_estimada', 'economia_anual_estimada'
        ]


class LeadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating leads"""
    
    class Meta:
        model = Lead
        fields = [
            'offer', 'consumo_medio_kwh', 'custo_medio_mensal',
            'melhor_horario_contato', 'observacoes', 'consentimento_lgpd'
        ]
    
    def validate_consentimento_lgpd(self, value):
        if not value:
            raise serializers.ValidationError(
                "Consentimento LGPD é obrigatório para criar lead"
            )
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['consentimento_data'] = timezone.now()
        return super().create(validated_data)


class LeadSerializer(serializers.ModelSerializer):
    """Serializer for lead details"""
    offer = OfferSerializer(read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            'id', 'offer', 'status', 'consumo_medio_kwh', 'custo_medio_mensal',
            'melhor_horario_contato', 'observacoes', 'consentimento_lgpd',
            'contatado_em', 'proposta_enviada_em', 'fechado_em',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'contatado_em', 'proposta_enviada_em', 'fechado_em',
            'created_at', 'updated_at'
        ]


class RenewableOptionsSerializer(serializers.Serializer):
    """Serializer for renewable energy options by CEP"""
    cep = serializers.CharField(max_length=9)
    consumo_medio_kwh = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )
    custo_medio_mensal = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )
    offers = OfferWithSavingsSerializer(many=True, read_only=True)
    total_offers = serializers.IntegerField(read_only=True)