#!/usr/bin/env python
import os
import django
import requests
import json
from io import BytesIO
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_simple')
django.setup()

BASE_URL = 'http://localhost:8000/api'

class APITester:
    def __init__(self):
        self.token = None
        self.user_id = None
        
    def test_register(self):
        """Teste de registro de usuário"""
        print("🧪 Testando registro...")
        data = {
            'username': 'teste_user',
            'email': 'teste@email.com',
            'password': 'senha123456',
            'first_name': 'Teste',
            'last_name': 'Usuario'
        }
        
        response = requests.post(f'{BASE_URL}/auth/register/', json=data)
        if response.status_code == 201:
            print("✅ Registro funcionando")
            return True
        else:
            print(f"❌ Erro no registro: {response.text}")
            return False
    
    def test_login(self):
        """Teste de login"""
        print("🧪 Testando login...")
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        response = requests.post(f'{BASE_URL}/auth/login/', json=data)
        if response.status_code == 200:
            result = response.json()
            self.token = result['access']
            self.user_id = result['user']['id']
            print("✅ Login funcionando")
            return True
        else:
            print(f"❌ Erro no login: {response.text}")
            return False
    
    def test_profile(self):
        """Teste de perfil"""
        print("🧪 Testando perfil...")
        headers = {'Authorization': f'Bearer {self.token}'}
        
        response = requests.get(f'{BASE_URL}/auth/profile/', headers=headers)
        if response.status_code == 200:
            print("✅ Perfil funcionando")
            return True
        else:
            print(f"❌ Erro no perfil: {response.text}")
            return False
    
    def test_upload(self):
        """Teste de upload"""
        print("🧪 Testando upload...")
        headers = {'Authorization': f'Bearer {self.token}'}
        
        # Criar imagem de teste
        img = Image.new('RGB', (800, 600), color='white')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        files = {'raw_file': ('conta_teste.jpg', img_bytes, 'image/jpeg')}
        
        response = requests.post(f'{BASE_URL}/bills/upload/', headers=headers, files=files)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Upload funcionando - Status: {result['status']}")
            return result['bill_id']
        else:
            print(f"❌ Erro no upload: {response.text}")
            return None
    
    def test_bills_list(self):
        """Teste de listagem de contas"""
        print("🧪 Testando listagem de contas...")
        headers = {'Authorization': f'Bearer {self.token}'}
        
        response = requests.get(f'{BASE_URL}/bills/', headers=headers)
        if response.status_code == 200:
            result = response.json()
            count = len(result.get('results', []))
            print(f"✅ Listagem funcionando - {count} contas encontradas")
            return True
        else:
            print(f"❌ Erro na listagem: {response.text}")
            return False
    
    def test_analytics(self):
        """Teste de analytics"""
        print("🧪 Testando analytics...")
        headers = {'Authorization': f'Bearer {self.token}'}
        
        response = requests.get(f'{BASE_URL}/analytics/summary/', headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analytics funcionando - {result['total_bills']} contas processadas")
            return True
        else:
            print(f"❌ Erro no analytics: {response.text}")
            return False
    
    def run_all_tests(self):
        """Executar todos os testes"""
        print("=" * 50)
        print("🚀 INICIANDO TESTES DA API")
        print("=" * 50)
        
        tests = [
            self.test_register,
            self.test_login,
            self.test_profile,
            self.test_upload,
            self.test_bills_list,
            self.test_analytics
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                print(f"❌ Erro no teste: {e}")
        
        print("\n" + "=" * 50)
        print(f"📊 RESULTADO: {passed}/{total} testes passaram")
        print("=" * 50)
        
        if passed == total:
            print("🎉 TODOS OS TESTES PASSARAM!")
            return True
        else:
            print("⚠️  ALGUNS TESTES FALHARAM!")
            return False

if __name__ == '__main__':
    tester = APITester()
    tester.run_all_tests()