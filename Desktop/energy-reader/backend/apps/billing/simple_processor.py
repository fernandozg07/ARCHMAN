import random
from decimal import Decimal
from datetime import datetime, timedelta

class SimpleProcessor:
    """Processador simples que simula OCR para demonstração"""
    
    def process_bill(self, file_path):
        """Simula processamento OCR e retorna dados realistas"""
        
        # Simular diferentes fornecedores
        fornecedores = ['ENEL SP', 'CPFL', 'CEMIG', 'LIGHT', 'COPEL']
        fornecedor = random.choice(fornecedores)
        
        # Gerar dados realistas
        consumo = Decimal(str(random.randint(150, 400)))
        tarifa = Decimal('0.75')  # R$ por kWh
        valor_energia = consumo * tarifa
        impostos = valor_energia * Decimal('0.3')  # 30% de impostos
        valor_total = valor_energia + impostos
        
        # Datas
        hoje = datetime.now().date()
        period_start = hoje - timedelta(days=30)
        period_end = hoje
        due_date = hoje + timedelta(days=15)
        
        return {
            'fornecedor': fornecedor,
            'numero_cliente': str(random.randint(100000000, 999999999)),
            'consumo_kwh': consumo,
            'tarifa_kwh': tarifa,
            'valor_total': valor_total,
            'period_start': period_start,
            'period_end': period_end,
            'due_date': due_date,
            'icms': impostos * Decimal('0.6'),
            'pis': impostos * Decimal('0.2'),
            'cofins': impostos * Decimal('0.2'),
            'bandeira_tarifaria': random.choice(['VERDE', 'AMARELA', 'VERMELHA']),
        }