@echo off
echo Configurando painel administrativo...

echo Criando migrações...
python manage.py makemigrations accounts
python manage.py makemigrations billing
python manage.py makemigrations analytics
python manage.py makemigrations renewables
python manage.py makemigrations audit

echo Aplicando migrações...
python manage.py migrate

echo Criando superusuário...
python create_admin.py

echo.
echo ✅ Painel administrativo configurado!
echo Acesse: http://localhost:8000/admin/
echo Usuario: admin
echo Senha: admin123
echo.
pause