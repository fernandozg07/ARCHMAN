# ARCHMAN - Energy Reader App

Sistema de gerenciamento de contas de energia com funcionalidades específicas por perfil de usuário.

## 🚀 Funcionalidades

### 👤 Usuário Comum
- Fotografar e processar contas de energia
- Visualizar dashboard pessoal
- Adicionar contas manualmente
- Gerenciar perfil

### 👮 Officer
- Todas as funcionalidades do usuário
- Painel financeiro com gestão de clientes
- Cadastro de novos officers
- Controle de comissões

### 👑 Administrador
- Acesso total ao sistema
- Painel administrativo
- Gerenciamento de usuários
- Relatórios e analytics

## 🛠️ Tecnologias

- React Native
- Expo
- TypeScript
- Zustand (State Management)
- React Navigation
- Expo Camera
- React Native Paper

## 📱 Instalação

```bash
# Clone o repositório
git clone https://github.com/fernandozg07/ARCHMAN.git

# Entre no diretório
cd ARCHMAN

# Instale as dependências
npm install

# Execute o projeto
npx expo start
```

## 🎨 Design System

- **Tema Escuro**: Background #1a1a2e, Surface #16213e
- **Cores por Perfil**:
  - User: Verde #00d4aa
  - Officer: Roxo #9c27b0  
  - Admin: Rosa #e91e63

## 📋 Estrutura do Projeto

```
src/
├── components/     # Componentes reutilizáveis
├── screens/        # Telas da aplicação
├── navigation/     # Configuração de navegação
├── services/       # API e serviços
├── store/          # Gerenciamento de estado
├── styles/         # Tema e estilos globais
└── types/          # Definições de tipos
```

## 🔐 Sistema de Permissões

O app implementa controle de acesso baseado em perfis, onde cada tipo de usuário tem acesso apenas às funcionalidades apropriadas.

## 🧪 Contas de Teste

- **Admin**: admin@admin.com / admin123
- **Officer**: officer@officer.com / officer123  
- **User**: user@user.com / user123

## 📄 Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.