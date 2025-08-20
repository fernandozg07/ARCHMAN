#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_simple')
django.setup()

from apps.billing.simple_processor import SimpleProcessor
from decimal import Decimal

def test_processor():
    """Testa o processador de contas"""
    print("🧪 Testando processador de contas...")
    
    try:
        processor = SimpleProcessor()
        
        # Simular processamento
        result = processor.process_bill("fake_path.jpg")
        
        # Verificar se retornou dados
        required_fields = ['fornecedor', 'numero_cliente', 'consumo_kwh', 'valor_total']
        
        print("✅ Dados extraídos:")
        for field in required_fields:
            value = result.get(field, 'N/A')
            print(f"   - {field}: {value}")
            
        # Verificar tipos
        assert isinstance(result['consumo_kwh'], Decimal), "Consumo deve ser Decimal"
        assert isinstance(result['valor_total'], Decimal), "Valor deve ser Decimal"
        assert result['fornecedor'] in ['ENEL SP', 'CPFL', 'CEMIG', 'LIGHT', 'COPEL'], "Fornecedor inválido"
        
        print("✅ Processador funcionando corretamente")
        return True
        
    except Exception as e:
        print(f"❌ Erro no processador: {e}")
        return False

def test_bill_creation():
    """Testa criação de conta no banco"""
    print("🧪 Testando criação de conta...")
    
    try:
        from apps.accounts.models import User
        from apps.billing.models import Bill
        
        # Pegar usuário admin
        user = User.objects.get(username='admin')
        
        # Criar conta de teste
        processor = SimpleProcessor()
        data = processor.process_bill("test.jpg")
        
        bill = Bill.objects.create(
            user=user,
            file_hash="test_hash_123",
            status='PROCESSED',
            **data
        )
        
        print(f"✅ Conta criada: ID {bill.id}")
        print(f"   - Fornecedor: {bill.fornecedor}")
        print(f"   - Valor: R$ {bill.valor_total}")
        print(f"   - Consumo: {bill.consumo_kwh} kWh")
        
        # Limpar teste
        bill.delete()
        print("✅ Conta de teste removida")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na criação: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("⚡ TESTANDO PROCESSAMENTO DE CONTAS")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    if test_processor():
        tests_passed += 1
        
    if test_bill_creation():
        tests_passed += 1
    
    print(f"\n📊 RESULTADO: {tests_passed}/{total_tests} testes passaram")
    
    if tests_passed == total_tests:
        print("🎉 PROCESSAMENTO OK!")
    else:
        print("❌ PROBLEMAS NO PROCESSAMENTO!")