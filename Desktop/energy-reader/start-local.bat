@echo off
echo ========================================
echo   ENERGY READER - DESENVOLVIMENTO LOCAL
echo ========================================

cd /d "c:\Users\ferna\Downloads\energy-reader (1)\energy-reader\backend"

echo.
echo [1/6] Verificando dependências...
pip install -r requirements.txt

echo.
echo [2/6] Criando migrações...
python manage.py makemigrations accounts
python manage.py makemigrations billing
python manage.py makemigrations analytics
python manage.py makemigrations renewables
python manage.py makemigrations audit
python manage.py makemigrations admin_panel
python manage.py makemigrations energy
python manage.py makemigrations

echo.
echo [3/6] Aplicando migrações...
python manage.py migrate

echo.
echo [4/6] Coletando arquivos estáticos...
python manage.py collectstatic --noinput

echo.
echo [5/6] Verificando configuração...
python manage.py check

echo.
echo [6/6] Iniciando servidor...
echo.
echo Servidor disponível em: http://localhost:8000
echo Admin disponível em: http://localhost:8000/admin/
echo API docs em: http://localhost:8000/api/docs/
echo.
python manage.py runserver 0.0.0.0:8000