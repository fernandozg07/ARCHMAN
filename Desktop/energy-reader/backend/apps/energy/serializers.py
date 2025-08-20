from rest_framework import serializers
from .models import Distributor, Officer, Client, Quote, CommercialProposal, FinancialRecord

class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = '__all__'

class OfficerSerializer(serializers.ModelSerializer):
    distributors = DistributorSerializer(many=True, read_only=True)
    distributor_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    
    class Meta:
        model = Officer
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }
    
    def create(self, validated_data):
        distributor_ids = validated_data.pop('distributor_ids', [])
        officer = Officer.objects.create(**validated_data)
        if distributor_ids:
            officer.distributors.set(distributor_ids)
        return officer

class ClientSerializer(serializers.ModelSerializer):
    distributor_name = serializers.CharField(source='distributor.name', read_only=True)
    officer_name = serializers.CharField(source='officer.full_name', read_only=True)
    
    class Meta:
        model = Client
        fields = '__all__'

class QuoteSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    officer_name = serializers.CharField(source='officer.full_name', read_only=True)
    
    class Meta:
        model = Quote
        fields = '__all__'

class CommercialProposalSerializer(serializers.ModelSerializer):
    quote_client_name = serializers.CharField(source='quote.client.name', read_only=True)
    
    class Meta:
        model = CommercialProposal
        fields = '__all__'

class FinancialRecordSerializer(serializers.ModelSerializer):
    officer_name = serializers.CharField(source='officer.full_name', read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    
    class Meta:
        model = FinancialRecord
        fields = '__all__'

class DashboardStatsSerializer(serializers.Serializer):
    total_clients = serializers.IntegerField()
    monthly_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    consolidated_remuneration = serializers.DecimalField(max_digits=12, decimal_places=2)
    pending_quotes = serializers.IntegerField()
    active_proposals = serializers.IntegerField()