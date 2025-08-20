# Energy Reader - Leitor Automático de Contas Enel

Sistema completo para leitura automática de contas de energia com OCR/ICR, analytics e marketplace de energias renováveis.

## 🚀 Stack Tecnológica

- **Backend**: Python 3.11, Django 5, DRF, PostgreSQL, Celery + Redis
- **OCR/ICR**: Tesseract/PaddleOCR + detecção de códigos de barras
- **Frontend Mobile**: React Native (Expo), TypeScript, Zustand
- **Admin**: Django Admin customizado
- **Deploy**: Railway + Docker

## 📁 Estrutura do Projeto

```
energy-reader/
├── backend/                 # Django API
├── mobile/                  # React Native (Expo)
├── infra/                   # Docker, scripts
├── docs/                    # Documentação
└── seeds/                   # Dados de exemplo
```

## 🛠️ Setup Desenvolvimento

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Redis

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata seeds/providers.json
```

### Mobile
```bash
cd mobile
npm install
npx expo start
```

### Docker (Desenvolvimento)
```bash
make dev  # Inicia todos os serviços
make test # Executa testes
make fmt  # Formata código
```

## 🚀 Deploy Railway

### 1. Preparação
```bash
# Instalar Railway CLI
npm install -g @railway/cli
railway login
```

### 2. Backend Deploy
```bash
cd backend
railway init
railway add postgresql
railway add redis
railway deploy
```

### 3. Variáveis de Ambiente
```bash
railway variables set SECRET_KEY=your-secret-key
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=your-domain.railway.app
railway variables set DATABASE_URL=postgresql://...
railway variables set REDIS_URL=redis://...
```

### 4. Migrações e Seeds
```bash
railway run python manage.py migrate
railway run python manage.py loaddata seeds/providers.json
railway run python manage.py createsuperuser
```

## 📱 Funcionalidades

### Cliente
- Upload de contas (câmera, galeria, PDF)
- Dashboard com KPIs e gráficos
- Histórico de consumo
- Marketplace de energias renováveis
- Geração de leads

### Admin
- Gerenciamento de usuários
- Reprocessamento de contas
- Auditoria e logs
- CRUD de fornecedores/ofertas

## 🔒 Segurança & LGPD

- Criptografia de arquivos em repouso
- JWT com refresh tokens
- MFA opcional (TOTP)
- Consentimento explícito para leads
- Logs de auditoria completos
- Rate limiting

## 📊 APIs Principais

- `POST /api/bills/upload` - Upload de conta
- `GET /api/bills/` - Lista de contas
- `GET /api/analytics/summary` - KPIs e métricas
- `GET /api/renewables/options` - Ofertas por CEP
- `POST /api/renewables/leads` - Criar lead

## 🧪 Testes

```bash
# Backend
cd backend
pytest --cov=. --cov-report=html

# Mobile
cd mobile
npm test
```

## 📄 Documentação API

Acesse `/api/schema/swagger-ui/` para documentação interativa OpenAPI.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT.