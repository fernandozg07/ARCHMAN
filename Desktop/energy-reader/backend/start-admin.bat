@echo off
echo Iniciando painel administrativo...
echo.

cd /d "%~dp0"

echo [INFO] Usando configuracao simplificada para admin
echo [INFO] Banco: admin.sqlite3
echo.

echo Iniciando servidor admin na porta 8000...
echo Acesse: http://localhost:8000/admin/
echo Usuario: admin
echo Senha: admin123
echo.
echo Pressione Ctrl+C para parar
echo.

python manage.py runserver --settings=config.settings_simple

pause