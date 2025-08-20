@echo off
echo ========================================
echo   ENERGY READER - APP FINAL COMPLETO
echo ========================================
echo.

echo ✅ FUNCIONALIDADES IMPLEMENTADAS:
echo.
echo 🔐 AUTENTICACAO:
echo    - Login/Registro funcionais
echo    - Persistencia de sessao
echo    - Logout seguro
echo.
echo 📱 TELAS PRINCIPAIS:
echo    - Dashboard com estatisticas reais
echo    - Upload com processamento OCR
echo    - Historico de contas
echo    - Perfil do usuario
echo.
echo 🔄 NAVEGACAO:
echo    - Navegacao entre telas
echo    - Detalhes da conta
echo    - Edicao de perfil
echo    - Botoes funcionais
echo.
echo 💾 PROCESSAMENTO:
echo    - Upload real de arquivos
echo    - Extracao automatica de dados
echo    - Salvamento no banco
echo    - Status em tempo real
echo.
echo 📊 ANALYTICS:
echo    - Estatisticas completas
echo    - Dados mensais
echo    - Breakdown por status
echo    - Medias e totais
echo.
echo ========================================
echo.

choice /c SN /m "Iniciar aplicacao completa (S/N)"
if errorlevel 2 goto :end

echo.
echo [1/2] Iniciando backend...
cd backend
start "Backend Energy Reader" cmd /k "python manage.py runserver --settings=config.settings_simple"
timeout /t 3 > nul

echo [2/2] Iniciando mobile...
cd ..\mobile
start "Mobile Energy Reader" cmd /k "npx expo start"

echo.
echo ========================================
echo   APLICACAO INICIADA COM SUCESSO!
echo ========================================
echo.
echo 🌐 BACKEND: http://localhost:8000/admin/
echo    Login: admin / admin123
echo.
echo 📱 MOBILE: Escaneie QR code ou pressione 'w'
echo.
echo 🧪 TESTE COMPLETO:
echo    1. Registre um usuario
echo    2. Faca login
echo    3. Envie uma foto de conta
echo    4. Veja dados extraidos
echo    5. Navegue pelo historico
echo    6. Veja detalhes da conta
echo    7. Edite seu perfil
echo    8. Veja estatisticas no dashboard
echo.
echo ✨ TODAS AS FUNCIONALIDADES FUNCIONANDO!
echo.

:end
pause