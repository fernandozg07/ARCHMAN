#!/usr/bin/env python
import os
import django
from decimal import Decimal
from datetime import datetime, timedelta
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_simple')
django.setup()

from apps.accounts.models import User
from apps.billing.models import Bill

# Criar usuários de exemplo
users_data = [
    {'username': 'joao.silva', 'email': 'joao@email.com', 'first_name': 'João', 'last_name': 'Silva'},
    {'username': 'maria.santos', 'email': 'maria@email.com', 'first_name': 'Maria', 'last_name': 'Santos'},
    {'username': 'pedro.costa', 'email': 'pedro@email.com', 'first_name': 'Pedro', 'last_name': 'Costa'},
]

for user_data in users_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'user_type': 'client',
            'is_verified': True
        }
    )
    if created:
        user.set_password('123456')
        user.save()
        print(f"Usuario criado: {user.username}")

# Criar contas de exemplo
bills_data = [
    {
        'fornecedor': 'ENEL SP',
        'numero_cliente': '123456789',
        'consumo_kwh': Decimal('245.50'),
        'valor_total': Decimal('189.75'),
        'status': 'PROCESSED',
        'file_hash': str(uuid.uuid4())[:32],
    },
    {
        'fornecedor': 'CPFL',
        'numero_cliente': '987654321',
        'consumo_kwh': Decimal('312.80'),
        'valor_total': Decimal('234.60'),
        'status': 'PROCESSED',
        'file_hash': str(uuid.uuid4())[:32],
    },
    {
        'fornecedor': 'ENEL RJ',
        'numero_cliente': '456789123',
        'consumo_kwh': Decimal('198.30'),
        'valor_total': Decimal('156.40'),
        'status': 'PROCESSING',
        'file_hash': str(uuid.uuid4())[:32],
    }
]

users = User.objects.filter(user_type='client')
for i, bill_data in enumerate(bills_data):
    if i < len(users):
        bill = Bill(user=users[i], **bill_data)
        bill.save()
        print(f"Conta criada: {bill.fornecedor} - R$ {bill.valor_total}")

print(f"\nDados criados!")
print(f"Usuarios: {User.objects.count()}")
print(f"Contas: {Bill.objects.count()}")