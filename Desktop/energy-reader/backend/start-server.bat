@echo off
echo Iniciando servidor Django...
echo.

cd /d "%~dp0"

echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Verificando configuracao...
python test_server.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Problemas na configuracao do Django!
    pause
    exit /b 1
)

echo.
echo Iniciando servidor na porta 8000...
echo Acesse: http://localhost:8000
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

python manage.py runserver

pause