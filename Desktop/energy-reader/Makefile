.PHONY: dev test fmt clean build deploy

# Desenvolvimento
dev:
	docker-compose up -d

dev-logs:
	docker-compose logs -f

dev-stop:
	docker-compose down

# Testes
test:
	cd backend && pytest --cov=. --cov-report=html
	cd mobile && npm test

test-backend:
	cd backend && pytest --cov=. --cov-report=html

test-mobile:
	cd mobile && npm test

# Formatação
fmt:
	cd backend && black . && flake8 .
	cd mobile && npm run lint:fix

# Limpeza
clean:
	docker-compose down -v
	docker system prune -f

# Build
build:
	docker-compose build

# Deploy
deploy-railway:
	cd backend && railway deploy

# Setup inicial
setup:
	cd backend && python -m venv venv && pip install -r requirements.txt
	cd mobile && npm install

# Migrações
migrate:
	cd backend && python manage.py migrate

# Seeds
seed:
	cd backend && python manage.py loaddata ../seeds/providers.json

# Superuser
superuser:
	cd backend && python manage.py createsuperuser