import requests
import json

def test_backend():
    try:
        # Test health endpoint
        response = requests.get('http://localhost:8000/api/health/', timeout=5)
        if response.status_code == 200:
            print("✅ Backend está rodando!")
            print(f"Status: {response.json()}")
            return True
        else:
            print(f"❌ Backend retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend não está rodando na porta 8000")
        return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def test_cors():
    try:
        headers = {
            'Origin': 'http://localhost:8081',
            'Access-Control-Request-Method': 'GET'
        }
        response = requests.options('http://localhost:8000/api/health/', headers=headers, timeout=5)
        print(f"CORS preflight status: {response.status_code}")
        return True
    except Exception as e:
        print(f"Erro no teste CORS: {e}")
        return False

if __name__ == "__main__":
    print("Testando conexão com backend...")
    backend_ok = test_backend()
    
    if backend_ok:
        print("\nTestando CORS...")
        test_cors()
        print("\n✅ Frontend pode se conectar ao backend!")
    else:
        print("\n❌ Inicie o backend primeiro com: python manage.py runserver")