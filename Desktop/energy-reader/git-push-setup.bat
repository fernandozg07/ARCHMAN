@echo off
echo ========================================
echo     CONFIGURANDO GIT PUSH
echo ========================================
echo.

echo Opcoes para fazer push:
echo.
echo 1. GitHub (recomendado)
echo 2. GitLab  
echo 3. Bitbucket
echo 4. Outro repositorio
echo.

choice /c 1234 /m "Escolha uma opcao"

if errorlevel 4 goto :outro
if errorlevel 3 goto :bitbucket  
if errorlevel 2 goto :gitlab
if errorlevel 1 goto :github

:github
echo.
echo Para GitHub:
echo 1. Crie um repositorio em: https://github.com/new
echo 2. Nome sugerido: energy-reader-app
echo 3. Execute os comandos:
echo.
echo git remote add origin https://github.com/SEU_USUARIO/energy-reader-app.git
echo git branch -M main
echo git push -u origin main
echo.
goto :end

:gitlab
echo.
echo Para GitLab:
echo 1. Crie um repositorio em: https://gitlab.com/projects/new
echo 2. Execute os comandos:
echo.
echo git remote add origin https://gitlab.com/SEU_USUARIO/energy-reader-app.git
echo git branch -M main  
echo git push -u origin main
echo.
goto :end

:bitbucket
echo.
echo Para Bitbucket:
echo 1. Crie um repositorio em: https://bitbucket.org/repo/create
echo 2. Execute os comandos:
echo.
echo git remote add origin https://bitbucket.org/SEU_USUARIO/energy-reader-app.git
echo git branch -M main
echo git push -u origin main
echo.
goto :end

:outro
echo.
echo Para outro repositorio:
echo git remote add origin URL_DO_SEU_REPOSITORIO
echo git push -u origin master
echo.
goto :end

:end
echo ========================================
echo.
echo Depois de configurar o remote, use:
echo git push origin master
echo.
echo Ou para forcar push:
echo git push -f origin master
echo.
pause