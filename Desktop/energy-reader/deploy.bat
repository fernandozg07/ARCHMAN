@echo off
echo 🚀 Iniciando deploy do Energy Reader...

echo.
echo 📦 1. Deploy Backend (Railway)
cd backend
echo Fazendo login no Railway...
railway login
echo Criando projeto...
railway init
echo Adicionando PostgreSQL...
railway add postgresql
echo Fazendo deploy...
railway up
echo Configurando variáveis...
railway variables set DEBUG=False
railway variables set SECRET_KEY=django-production-key-change-me
cd ..

echo.
echo 🌐 2. Deploy Frontend (Vercel)
cd energy-reader-app
echo Instalando Vercel CLI...
npm install -g vercel
echo Fazendo deploy...
vercel --prod
cd ..

echo.
echo ✅ Deploy concluído!
echo Backend: Verifique o URL no Railway
echo Frontend: Verifique o URL no Vercel
pause