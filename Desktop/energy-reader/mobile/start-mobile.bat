@echo off
echo Iniciando app mobile...
echo.

cd /d "%~dp0"

echo Verificando dependencias...
if not exist node_modules (
    echo Instalando dependencias...
    npm install
)

echo.
echo Iniciando Expo...
echo Escaneie o QR code com o app Expo Go
echo Ou pressione 'w' para abrir no navegador
echo.

npx expo start

pause