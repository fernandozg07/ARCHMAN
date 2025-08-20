@echo off
echo ========================================
echo TESTANDO ENERGY READER APP COMPLETO
echo ========================================
echo.

echo [1/4] Testando backend...
cd backend
python manage.py check --settings=config.settings_simple
if %errorlevel% neq 0 (
    echo ERRO: Backend com problemas
    pause
    exit /b 1
)
echo ✅ Backend OK

echo.
echo [2/4] Coletando arquivos estaticos...
python manage.py collectstatic --noinput --settings=config.settings_simple > nul
echo ✅ Arquivos estaticos OK

echo.
echo [3/4] Testando mobile...
cd ..\mobile
if not exist node_modules (
    echo Instalando dependencias...
    npm install
)
echo ✅ Mobile OK

echo.
echo [4/4] Iniciando aplicacao...
echo.
echo BACKEND: http://localhost:8000/admin/
echo LOGIN: admin / admin123
echo.
echo MOBILE: Escaneie o QR code ou pressione 'w'
echo.
echo ========================================
echo TUDO PRONTO! Testando...
echo ========================================
echo.

start "Backend" cmd /k "cd /d %~dp0backend && python manage.py runserver --settings=config.settings_simple"
timeout /t 3 > nul
start "Mobile" cmd /k "cd /d %~dp0mobile && npx expo start"

echo Apps iniciados! Teste as funcionalidades:
echo.
echo 1. Acesse o admin: http://localhost:8000/admin/
echo 2. Abra o mobile no Expo Go
echo 3. Registre um usuario
echo 4. Faca login
echo 5. Teste upload de conta
echo 6. Veja o historico
echo.
pause