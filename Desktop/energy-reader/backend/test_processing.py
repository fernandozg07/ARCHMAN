#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_simple')
django.setup()

from apps.billing.simple_processor import SimpleProcessor
from decimal import Decimal

def test_processor():
    """Testa o processador de contas"""
    print("Testando processador de contas...")
    
    try:
        processor = SimpleProcessor()
        
        # Simular processamento
        result = processor.process_bill("fake_path.jpg")
        
        # Verificar se retornou dados
        required_fields = ['fornecedor', 'numero_cliente', 'consumo_kwh', 'valor_total']
        
        print("OK Dados extraidos:")
        for field in required_fields:
            value = result.get(field, 'N/A')
            print(f"   - {field}: {value}")
            
        # Verificar tipos
        assert isinstance(result['consumo_kwh'], Decimal), "Consumo deve ser Decimal"
        assert isinstance(result['valor_total'], Decimal), "Valor deve ser Decimal"
        assert result['fornecedor'] in ['ENEL SP', 'CPFL', 'CEMIG', 'LIGHT', 'COPEL'], "Fornecedor invalido"
        
        print("OK Processador funcionando corretamente")
        return True
        
    except Exception as e:
        print(f"ERRO no processador: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("TESTANDO PROCESSAMENTO DE CONTAS")
    print("=" * 50)
    
    if test_processor():
        print("\nPROCESSAMENTO OK!")
    else:
        print("\nPROBLEMAS NO PROCESSAMENTO!")