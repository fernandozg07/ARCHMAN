@echo off
echo Corrigindo problemas de desenvolvimento local...

cd /d "c:\Users\ferna\Downloads\energy-reader (1)\energy-reader\backend"

echo.
echo 1. Verificando SECRET_KEY...
python -c "from django.core.management.utils import get_random_secret_key; print('SECRET_KEY=' + get_random_secret_key())" > temp_key.txt

echo.
echo 2. Criando migrações...
python manage.py makemigrations

echo.
echo 3. Aplicando migrações...
python manage.py migrate

echo.
echo 4. Coletando arquivos estáticos...
python manage.py collectstatic --noinput

echo.
echo 5. Criando superusuário (opcional)...
echo Para criar um superusuário, execute: python manage.py createsuperuser

echo.
echo 6. Testando servidor...
echo Iniciando servidor de desenvolvimento...
python manage.py runserver 0.0.0.0:8000

pause