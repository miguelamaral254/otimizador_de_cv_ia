# Otimizador de Currículos com IA - Frontend

Este é o frontend da aplicação "Otimizador de Currículos com IA", desenvolvido em React com TypeScript.

## Estrutura do Projeto

```
/src
├── /api                    # Configuração e serviços de API
│   └── apiClient.ts       # Configuração do Axios para comunicação com o backend
├── /components            # Componentes React reutilizáveis
│   ├── /common           # Componentes comuns (Button, Input, Modal)
│   └── /layout           # Componentes de estrutura (Navbar, Sidebar)
├── /hooks                 # Hooks customizados (useAuth, etc.)
├── /pages                 # Páginas da aplicação
│   ├── Dashboard.tsx     # Página principal do dashboard
│   ├── LoginPage.tsx     # Página de login (em desenvolvimento)
│   └── RegisterPage.tsx  # Página de cadastro (em desenvolvimento)
├── /router               # Configuração de rotas
│   └── index.tsx         # Configuração das rotas com React Router DOM
├── /store                # Estado global da aplicação
│   └── userStore.ts      # Store de usuário com Zustand
└── App.tsx               # Componente principal da aplicação
```

## Tecnologias Utilizadas

- **React 19** - Biblioteca para construção de interfaces
- **TypeScript** - Superset do JavaScript com tipagem estática
- **Vite** - Build tool e dev server
- **React Router DOM** - Roteamento da aplicação
- **Zustand** - Gerenciamento de estado global
- **Axios** - Cliente HTTP para comunicação com APIs
- **Tailwind CSS** - Framework CSS utilitário (classes simuladas)

## Funcionalidades Implementadas

### ✅ Estrutura Base
- Organização de pastas seguindo boas práticas
- Configuração de rotas com proteção de acesso
- Sistema de autenticação básico (simulado)
- Componentes reutilizáveis de exemplo

### 🚧 Em Desenvolvimento
- Páginas de login e cadastro
- Upload de arquivos PDF
- Análise de currículos com IA
- Histórico de versões
- Dashboard completo

## Como Executar

### Pré-requisitos
- Node.js 18+ 
- npm ou yarn

### Instalação
```bash
# Instalar dependências
npm install

# Executar em modo de desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview da build
npm run preview
```

### Variáveis de Ambiente
Crie um arquivo `.env.local` na raiz do projeto:
```env
VITE_API_URL=http://localhost:8000
```

## Desenvolvimento

### Adicionando Novos Componentes
1. Crie o componente na pasta apropriada (`/components/common` ou `/components/layout`)
2. Exporte-o no arquivo `index.ts` da pasta
3. Importe e use onde necessário

### Adicionando Novas Páginas
1. Crie a página em `/pages`
2. Adicione a rota em `/router/index.tsx`
3. Configure proteção de acesso se necessário

### Adicionando Novos Hooks
1. Crie o hook em `/hooks`
2. Use o padrão de nomenclatura `use[Nome]`
3. Exporte funcionalidades específicas

## Arquitetura

### Estado Global
- **Zustand**: Gerenciamento de estado simples e eficiente
- **Stores separados**: Cada domínio tem seu próprio store
- **Persistência**: Tokens de autenticação no localStorage

### Roteamento
- **React Router DOM**: Roteamento declarativo
- **Rotas protegidas**: Acesso restrito a usuários autenticados
- **Redirecionamento automático**: Baseado no estado de autenticação

### Comunicação com API
- **Axios**: Cliente HTTP configurável
- **Interceptors**: Tratamento automático de tokens e erros
- **Base URL configurável**: Via variáveis de ambiente

## Próximos Passos

1. **Implementar páginas de autenticação** completas
2. **Criar sistema de upload** de arquivos PDF
3. **Integrar com backend** para análise de currículos
4. **Implementar dashboard** com gráficos e métricas
5. **Adicionar testes** unitários e de integração
6. **Configurar CI/CD** para deploy automático

## Contribuição

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto é parte do desafio técnico do time de desenvolvimento.
