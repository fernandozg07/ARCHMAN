// Teste básico do mobile
const API_BASE = 'http://localhost:8000/api';

async function testMobileAPI() {
    console.log('🧪 Testando API do mobile...');
    
    try {
        // Teste de conectividade
        const response = await fetch(`${API_BASE}/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: 'admin',
                password: 'admin123'
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Conectividade OK');
            console.log('✅ Token recebido:', data.access ? 'Sim' : 'Não');
            console.log('✅ Usuário:', data.user?.username || 'N/A');
            return true;
        } else {
            console.log('❌ Erro na conectividade:', response.status);
            return false;
        }
    } catch (error) {
        console.log('❌ Erro de rede:', error.message);
        return false;
    }
}

// Executar teste
testMobileAPI().then(success => {
    if (success) {
        console.log('\n🎉 MOBILE API OK!');
    } else {
        console.log('\n❌ PROBLEMAS NA API MOBILE!');
    }
});