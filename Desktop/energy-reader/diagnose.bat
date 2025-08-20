@echo off
echo ========================================
echo   DIAGNÓSTICO - ENERGY READER
echo ========================================

cd /d "c:\Users\ferna\Downloads\energy-reader (1)\energy-reader\backend"

echo.
echo [VERIFICANDO PYTHON]
python --version
echo.

echo [VERIFICANDO DJANGO]
python -c "import django; print('Django:', django.get_version())"
echo.

echo [VERIFICANDO DEPENDÊNCIAS]
python -c "
try:
    import rest_framework
    print('✓ Django REST Framework OK')
except ImportError:
    print('✗ Django REST Framework FALTANDO')

try:
    import corsheaders
    print('✓ CORS Headers OK')
except ImportError:
    print('✗ CORS Headers FALTANDO')

try:
    import decouple
    print('✓ Python Decouple OK')
except ImportError:
    print('✗ Python Decouple FALTANDO')
"
echo.

echo [VERIFICANDO CONFIGURAÇÃO]
python manage.py check --deploy
echo.

echo [VERIFICANDO MIGRAÇÕES]
python manage.py showmigrations
echo.

echo [VERIFICANDO BANCO DE DADOS]
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    print('✓ Conexão com banco OK')
except Exception as e:
    print('✗ Erro na conexão:', e)
"

echo.
echo ========================================
echo   DIAGNÓSTICO CONCLUÍDO
echo ========================================
pause