#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@energyreader.com',
        password='admin123',
        user_type='admin'
    )
    print("[OK] Superusuario criado!")
    print("Username: admin")
    print("Password: admin123")
else:
    print("[INFO] Superusuario ja existe")