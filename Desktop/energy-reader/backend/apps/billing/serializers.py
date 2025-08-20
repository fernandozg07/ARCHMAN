from rest_framework import serializers
from .models import Bill

class BillUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['raw_file']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class BillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'status', 'fornecedor', 'period_start', 'period_end', 
                 'consumo_kwh', 'valor_total', 'created_at']

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'
        read_only_fields = ['user', 'file_hash', 'created_at', 'updated_at']