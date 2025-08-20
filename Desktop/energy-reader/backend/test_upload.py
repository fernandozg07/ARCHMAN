#!/usr/bin/env python
import os
import django
import requests
from io import BytesIO
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_simple')
django.setup()

# Criar uma imagem de teste
def create_test_image():
    img = Image.new('RGB', (800, 600), color='white')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

# Testar upload
def test_upload():
    # Primeiro fazer login
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)
    if response.status_code != 200:
        print(f"Erro no login: {response.text}")
        return
    
    token = response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Fazer upload de imagem de teste
    img_bytes = create_test_image()
    files = {'raw_file': ('conta_teste.jpg', img_bytes, 'image/jpeg')}
    
    response = requests.post('http://localhost:8000/api/bills/upload/', 
                           headers=headers, files=files)
    
    if response.status_code == 201:
        data = response.json()
        print("✅ Upload realizado com sucesso!")
        print(f"ID da conta: {data['bill_id']}")
        print(f"Status: {data['status']}")
        print(f"Dados extraídos: {data.get('data', {})}")
    else:
        print(f"❌ Erro no upload: {response.text}")

if __name__ == '__main__':
    test_upload()