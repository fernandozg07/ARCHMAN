#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    # Test if Django can start
    try:
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        print("[OK] Django configurado corretamente!")
        print("[INFO] Servidor pode ser iniciado com: python manage.py runserver")
        
        # Test database connection
        from django.db import connection
        cursor = connection.cursor()
        print("[OK] Conexao com banco de dados OK!")
        
    except Exception as e:
        print(f"[ERRO] {e}")
        sys.exit(1)