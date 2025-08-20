#!/usr/bin/env python
import os
import sqlite3

# Remove database file
db_path = 'db.sqlite3'
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("✅ Banco de dados removido")
    except Exception as e:
        print(f"❌ Erro ao remover banco: {e}")

# Remove migration files (keep __init__.py)
apps = ['accounts', 'billing', 'analytics', 'renewables', 'audit']
for app in apps:
    migrations_dir = f'apps/{app}/migrations'
    if os.path.exists(migrations_dir):
        for file in os.listdir(migrations_dir):
            if file.endswith('.py') and file != '__init__.py':
                try:
                    os.remove(os.path.join(migrations_dir, file))
                    print(f"✅ Removido {app}/migrations/{file}")
                except Exception as e:
                    print(f"❌ Erro ao remover {file}: {e}")

print("✅ Reset completo!")
print("Execute: python manage.py makemigrations && python manage.py migrate")