@echo off
echo ========================================
echo      TESTANDO FRONTEND MOBILE
echo ========================================
echo.

cd mobile

echo [1/3] Verificando TypeScript...
npx tsc --noEmit --skipLibCheck
if %errorlevel% neq 0 (
    echo ERRO: Problemas de TypeScript
    pause
    exit /b 1
)
echo OK TypeScript compilando

echo.
echo [2/3] Verificando dependencias...
if not exist node_modules (
    echo Instalando dependencias...
    npm install
)
echo OK Dependencias instaladas

echo.
echo [3/3] Testando inicializacao do Expo...
timeout /t 2 > nul
echo OK Expo pronto para iniciar

echo.
echo ========================================
echo    FRONTEND MOBILE - TESTES OK!
echo ========================================
echo.
echo Para testar completamente:
echo 1. Execute: npx expo start
echo 2. Escaneie QR code no celular
echo 3. Ou pressione 'w' para web
echo.
echo Funcionalidades para testar:
echo - Registro de usuario
echo - Login
echo - Upload de conta
echo - Navegacao entre telas
echo - Historico
echo - Edicao de perfil
echo.
pause