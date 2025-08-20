@echo off
echo ========================================
echo    EXECUTANDO TODOS OS TESTES
echo ========================================
echo.

echo [1/4] Verificando se o servidor esta rodando...
curl -s http://localhost:8000/admin/ > nul
if %errorlevel% neq 0 (
    echo ❌ Servidor nao esta rodando!
    echo Inicie o servidor primeiro: cd backend && start-admin.bat
    pause
    exit /b 1
)
echo ✅ Servidor rodando

echo.
echo [2/4] Testando banco de dados...
cd backend
python test_database.py

echo.
echo [3/4] Testando endpoints da API...
python test_api_endpoints.py

echo.
echo [4/4] Testando conectividade mobile...
cd ..\mobile
node test_mobile.js

echo.
echo ========================================
echo       TESTES CONCLUIDOS
echo ========================================
echo.
echo Agora teste manualmente:
echo 1. Abra o mobile: npx expo start
echo 2. Registre um usuario
echo 3. Faca login
echo 4. Envie uma conta
echo 5. Veja o historico
echo 6. Edite o perfil
echo.
pause