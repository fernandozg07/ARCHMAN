# 🚀 Deploy Energy Reader

## Backend (Railway)

### 1. Instalar Railway CLI
```bash
npm install -g @railway/cli
```

### 2. Login e Deploy
```bash
cd backend
railway login
railway init
railway add postgresql
railway up
```

### 3. Configurar Variáveis
```bash
railway variables set DEBUG=False
railway variables set SECRET_KEY=sua-chave-secreta-aqui
railway variables set ALLOWED_HOSTS=*.railway.app
```

### 4. Executar Migrações
```bash
railway run python manage.py migrate --settings=config.settings_simple
railway run python manage.py createsuperuser --settings=config.settings_simple
```

## Frontend (Vercel)

### 1. Instalar Vercel CLI
```bash
npm install -g vercel
```

### 2. Deploy
```bash
cd energy-reader-app
vercel --prod
```

### 3. Configurar Domínio (Opcional)
- Acesse dashboard.vercel.com
- Configure domínio personalizado

## Alternativa: Netlify

### Frontend (Netlify)
```bash
cd energy-reader-app
npm run build:web
# Upload pasta dist/ para Netlify
```

## URLs Finais

Após deploy:
- **Backend**: https://seu-projeto.up.railway.app
- **Frontend**: https://seu-projeto.vercel.app
- **Admin**: https://seu-projeto.up.railway.app/admin

## Teste de Funcionamento

1. Acesse frontend
2. Teste navegação entre telas
3. Verifique API: `/api/health/`
4. Acesse admin Django

## Troubleshooting

### Erro de CORS
Adicione domínio frontend em `ALLOWED_HOSTS`

### Erro de Static Files
Configure `STATIC_ROOT` no settings

### Erro de Database
Verifique `DATABASE_URL` no Railway