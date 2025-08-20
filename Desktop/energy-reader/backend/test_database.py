#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_simple')
django.setup()

from apps.accounts.models import User
from apps.billing.models import Bill

def test_database():
    """Testa conexão e dados do banco"""
    print("Testando banco de dados...")
    
    try:
        # Teste de usuários
        user_count = User.objects.count()
        admin_exists = User.objects.filter(username='admin').exists()
        
        print(f"OK Usuarios no banco: {user_count}")
        print(f"OK Admin existe: {admin_exists}")
        
        # Teste de contas
        bill_count = Bill.objects.count()
        processed_bills = Bill.objects.filter(status='PROCESSED').count()
        
        print(f"OK Contas no banco: {bill_count}")
        print(f"OK Contas processadas: {processed_bills}")
        
        # Teste de dados recentes
        recent_bills = Bill.objects.order_by('-created_at')[:3]
        print(f"OK Ultimas 3 contas:")
        for bill in recent_bills:
            print(f"   - {bill.fornecedor or 'N/A'} - R$ {bill.valor_total or 0} - {bill.status}")
        
        return True
        
    except Exception as e:
        print(f"ERRO no banco: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("TESTANDO BANCO DE DADOS")
    print("=" * 50)
    
    if test_database():
        print("\nBANCO DE DADOS OK!")
    else:
        print("\nPROBLEMAS NO BANCO!")