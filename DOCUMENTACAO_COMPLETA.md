# 📚 Documentação Completa - Otimizador de Currículos com IA

## 🎯 Visão Geral do Projeto

O **Otimizador de Currículos com IA** é uma plataforma SaaS completa que permite aos usuários fazer upload de currículos em PDF, receber análises detalhadas geradas por IA e acompanhar a evolução da qualidade de seus currículos ao longo do tempo.

### 🏗️ Arquitetura Geral

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Banco de      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   Dados         │
│                 │    │                 │    │   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🚀 Backend (FastAPI)

### 📁 Estrutura de Diretórios

```
backend/
├── app/
│   ├── core/          # Configurações e utilitários centrais
│   ├── models/        # Modelos de banco de dados
│   ├── routers/       # Rotas da API
│   ├── schemas/       # Schemas Pydantic
│   └── utils/         # Utilitários
├── main.py            # Ponto de entrada da aplicação
├── init_db.py         # Script de inicialização do banco
├── pyproject.toml     # Dependências e configurações
└── .env.example       # Variáveis de ambiente de exemplo
```

### 🔧 Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para Python
- **SQLAlchemy**: ORM para banco de dados
- **Pydantic**: Validação de dados e serialização
- **SQLite**: Banco de dados (desenvolvimento)
- **Uvicorn**: Servidor ASGI
- **spaCy**: Processamento de linguagem natural
- **Google Gemini**: API de IA para análise de currículos

### 📊 Modelos de Dados

#### User (Usuário)
- `id`: Identificador único
- `email`: Email do usuário
- `password_hash`: Hash da senha
- `created_at`: Data de criação
- `updated_at`: Data de atualização

#### Curriculum (Currículo)
- `id`: Identificador único
- `user_id`: Referência ao usuário
- `filename`: Nome do arquivo
- `file_path`: Caminho do arquivo
- `upload_date`: Data de upload
- `analysis_result`: Resultado da análise

#### Metrics (Métricas)
- `id`: Identificador único
- `curriculum_id`: Referência ao currículo
- `action_verbs_score`: Pontuação de verbos de ação
- `quantification_score`: Pontuação de quantificação
- `overall_score`: Pontuação geral
- `created_at`: Data de criação

### 🛣️ Endpoints da API

#### Autenticação (`/api/auth`)
- `POST /register`: Cadastro de usuário
- `POST /login`: Login de usuário
- `POST /logout`: Logout de usuário

#### Currículos (`/api/curriculum`)
- `POST /upload`: Upload de currículo
- `GET /list`: Lista de currículos do usuário
- `GET /{id}`: Detalhes de um currículo
- `DELETE /{id}`: Remoção de currículo

#### Métricas (`/api/metrics`)
- `GET /history`: Histórico de métricas
- `GET /progress`: Progresso do usuário
- `GET /analytics`: Análises detalhadas

### 🔐 Segurança

- **JWT**: Autenticação baseada em tokens
- **CORS**: Configuração de origens permitidas
- **Trusted Host**: Validação de hosts
- **Hash de Senhas**: Bcrypt para segurança

### 📁 Configurações

#### Variáveis de Ambiente (.env)
```bash
# Backend
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000

# Banco de Dados
DATABASE_URL=sqlite+aiosqlite:///./otimizador_cv.db

# Segurança
SECRET_KEY=sua-chave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# IA
GEMINI_API_KEY=sua-chave-api-gemini

# Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760

# spaCy
SPACY_MODEL=pt_core_news_sm
```

---

## 🎨 Frontend (React)

### 📁 Estrutura de Diretórios

```
frontend/
├── src/
│   ├── api/           # Cliente HTTP e configurações
│   ├── components/    # Componentes reutilizáveis
│   ├── pages/         # Páginas da aplicação
│   ├── stores/        # Gerenciamento de estado (Zustand)
│   ├── utils/         # Utilitários
│   ├── App.jsx        # Componente principal
│   └── main.jsx       # Ponto de entrada
├── public/             # Arquivos estáticos
├── package.json        # Dependências
└── tailwind.config.js  # Configuração do Tailwind CSS
```

### 🔧 Tecnologias Utilizadas

- **React 18**: Biblioteca para interfaces de usuário
- **React Router**: Roteamento da aplicação
- **Vite**: Build tool e dev server
- **Tailwind CSS**: Framework CSS utilitário
- **Zustand**: Gerenciamento de estado
- **Axios**: Cliente HTTP
- **React Dropzone**: Upload de arquivos
- **Recharts**: Gráficos e visualizações
- **React Hot Toast**: Notificações

### 🧩 Componentes Principais

#### Header
- Navegação principal
- Menu de usuário autenticado
- Logo e branding

#### Footer
- Links úteis
- Informações de contato
- Copyright

#### Dashboard
- Upload de currículos
- Visualização de métricas
- Histórico de análises

#### UploadArea
- Drag & drop de arquivos
- Validação de formato
- Barra de progresso

#### MetricsChart
- Gráficos de evolução
- Comparação de versões
- Indicadores de progresso

### 🛣️ Rotas da Aplicação

- `/`: Página inicial
- `/about`: Sobre o projeto
- `/contact`: Contato
- `/dashboard`: Dashboard principal (protegido)
- `/upload`: Upload de currículos (protegido)
- `/history`: Histórico de análises (protegido)

### 🎨 Design System

#### Cores
- **Primária**: Azul (#3B82F6)
- **Secundária**: Verde (#10B981)
- **Aviso**: Amarelo (#F59E0B)
- **Erro**: Vermelho (#EF4444)
- **Neutro**: Cinza (#6B7280)

#### Tipografia
- **Títulos**: Inter, sans-serif
- **Corpo**: Inter, sans-serif
- **Monospace**: JetBrains Mono

#### Componentes
- Botões com estados hover/focus
- Cards com sombras sutis
- Formulários com validação visual
- Modais responsivos

### 📱 Responsividade

- **Mobile First**: Design otimizado para dispositivos móveis
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)
- **Grid System**: Flexbox e CSS Grid
- **Touch Friendly**: Elementos otimizados para toque

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- **Python 3.11+**
- **Node.js 18+**
- **npm ou yarn**

### Backend

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd otimizador_de_cv_ia/backend
```

2. **Crie um ambiente virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -e .
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Inicialize o banco de dados**
```bash
python init_db.py
```

6. **Execute a aplicação**
```bash
python main.py
```

### Frontend

1. **Navegue para o diretório do frontend**
```bash
cd ../frontend
```

2. **Instale as dependências**
```bash
npm install
```

3. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. **Execute em modo de desenvolvimento**
```bash
npm run dev
```

5. **Build para produção**
```bash
npm run build
```

---

## 🧪 Testes

### Backend
```bash
cd backend
pytest test_metrics_api.py -v
```

### Frontend
```bash
cd frontend
npm run lint
```

---

## 📊 Funcionalidades Implementadas

### ✅ Backend
- [x] Estrutura base FastAPI
- [x] Sistema de autenticação JWT
- [x] Modelos de banco de dados
- [x] Rotas para currículos e métricas
- [x] Configuração de CORS e segurança
- [x] Sistema de logging
- [x] Validação de arquivos
- [x] Integração com spaCy para NLP
- [x] **Upload e análise de currículos PDF**
- [x] **Análise estrutural com spaCy (verbos, quantificação)**
- [x] **Integração com Google Gemini para feedback qualitativo**
- [x] **Sistema de pontuação automática**
- [x] **Análise de palavras-chave baseada em descrição de vaga**

### ✅ Frontend
- [x] Estrutura base React
- [x] Roteamento com React Router
- [x] Componentes base (Header, Footer)
- [x] Páginas principais (Home, About, Contact)
- [x] Configuração Tailwind CSS
- [x] Sistema de build com Vite
- [x] Cliente HTTP com Axios

### 🔄 Em Desenvolvimento
- [ ] Upload de arquivos PDF
- [ ] Análise de currículos com IA
- [ ] Dashboard de métricas
- [ ] Gráficos de progresso
- [ ] Sistema de notificações
- [ ] Histórico de versões

---

## 🚧 Próximos Passos

### Backend
1. ✅ **Implementar análise de currículos com spaCy** - Concluído
2. ✅ **Integrar com Google Gemini API** - Concluído
3. ✅ **Sistema de upload e análise de PDFs** - Concluído
4. Adicionar cache Redis para performance
5. Implementar testes unitários completos
6. Adicionar documentação OpenAPI detalhada

### Frontend
1. Implementar sistema de autenticação
2. Criar dashboard principal
3. Implementar upload de arquivos
4. Adicionar visualizações de métricas
5. Implementar sistema de notificações

### DevOps
1. Configurar CI/CD
2. Adicionar Docker
3. Configurar monitoramento
4. Implementar backup automático
5. Configurar ambiente de staging

---

## 📝 Contribuição

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🤝 Suporte

Para dúvidas ou suporte:
- Abra uma issue no GitHub
- Entre em contato através da página de contato
- Consulte a documentação da API em `/docs`

---

*Última atualização: Dezembro 2024*
