@echo off
echo ========================================
echo TESTANDO PROCESSAMENTO REAL DE CONTAS
echo ========================================
echo.

cd backend

echo [1/3] Iniciando servidor...
start "Backend" cmd /k "python manage.py runserver --settings=config.settings_simple"
timeout /t 5 > nul

echo [2/3] Testando upload e processamento...
python test_upload.py

echo.
echo [3/3] Verificando dados no admin...
echo Acesse: http://localhost:8000/admin/billing/bill/
echo Login: admin / admin123
echo.
echo ========================================
echo TESTE CONCLUIDO!
echo ========================================
echo.
echo Agora teste no mobile:
echo 1. cd mobile && start-mobile.bat
echo 2. Registre um usuario
echo 3. Faca upload de uma foto
echo 4. Veja os dados extraidos automaticamente!
echo.
pause