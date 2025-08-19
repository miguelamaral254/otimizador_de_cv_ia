# ⚙️ Configuração do Projeto Full-Stack

## 📋 Informações Técnicas

### Versões das Tecnologias

#### Frontend
- **Node.js**: 18.0.0+
- **npm**: 9.0.0+
- **React**: 18.2.0
- **Vite**: 5.0.0
- **Tailwind CSS**: 3.3.6

#### Backend
- **Python**: 3.11.5+
- **FastAPI**: 0.104.0+
- **SQLAlchemy**: 2.0.0+
- **Uvicorn**: 0.24.0+
- **PyMuPDF**: 1.23.0+

### Estrutura de Pastas
```
otimizador_de_cv_ia/
├── frontend/                 # Frontend React
│   ├── src/
│   │   ├── components/      # Componentes reutilizáveis
│   │   ├── pages/           # Páginas da aplicação
│   │   ├── App.jsx          # Componente principal
│   │   ├── main.jsx         # Ponto de entrada
│   │   └── index.css        # Estilos globais
│   ├── public/              # Arquivos estáticos
│   ├── package.json         # Dependências Node.js
│   ├── vite.config.js       # Configuração do Vite
│   ├── tailwind.config.js   # Configuração do Tailwind
│   └── README.md            # Documentação
└── backend/                  # Backend FastAPI (Python)
    ├── app/                  # Código da aplicação
    │   ├── core/            # Configurações centrais
    │   ├── models/          # Modelos SQLAlchemy
    │   ├── schemas/         # Schemas Pydantic
    │   ├── api/             # Rotas da API
    │   ├── services/        # Lógica de negócio
    │   └── utils/           # Utilitários
    ├── main.py              # Ponto de entrada
    ├── pyproject.toml       # Configuração do projeto
    ├── requirements.txt     # Dependências Python
    └── README.md            # Documentação
```

## 🔧 Configurações de Desenvolvimento

### Variáveis de Ambiente

#### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
VITE_APP_NAME="Otimizador de Currículos com IA"
VITE_DEBUG_MODE=true
VITE_LOG_LEVEL=info
```

#### Backend (.env)
```bash
# Configurações da API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG_MODE=true

# Configurações de IA
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Configurações de segurança
SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configurações do banco
DATABASE_URL=sqlite:///./cv_optimizer.db

# Configurações de upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB
```

### Scripts NPM (Frontend)
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx"
  }
}
```

### Scripts Python (Backend)
```bash
# Executar servidor de desenvolvimento
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Executar testes
pytest

# Executar linting
flake8 app/
black app/
isort app/
```

### Configuração do Vite
```javascript
// vite.config.js
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})
```

### Configuração do FastAPI
```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Otimizador de Currículos com IA",
    description="API para análise e otimização de currículos usando IA",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Configuração do Tailwind
```javascript
// tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        secondary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
```

## 🎨 Design System

### Cores Principais
- **Primary**: Azul (#3b82f6)
- **Secondary**: Cinza (#64748b)
- **Success**: Verde (#10b981)
- **Warning**: Amarelo (#f59e0b)
- **Error**: Vermelho (#ef4444)

### Tipografia
- **Fonte Principal**: Inter
- **Tamanhos**: text-xs, text-sm, text-base, text-lg, text-xl, text-2xl, text-3xl, text-4xl
- **Pesos**: font-light, font-normal, font-medium, font-semibold, font-bold

### Espaçamentos
- **Container**: max-w-7xl, mx-auto, px-4
- **Seções**: py-8, py-12, py-16
- **Cards**: p-6, p-8
- **Gaps**: gap-4, gap-6, gap-8

## 📱 Responsividade

### Breakpoints
- **Mobile**: < 640px (sm:)
- **Tablet**: 640px - 1024px (md:)
- **Desktop**: > 1024px (lg:)

### Classes Responsivas
```jsx
<div className="
  grid 
  grid-cols-1 
  md:grid-cols-2 
  lg:grid-cols-3 
  gap-4
">
  {/* Conteúdo responsivo */}
</div>
```

## 🔐 Autenticação

### Estrutura de Estado (Frontend)
```javascript
// authStore.js
{
  user: null,
  token: null,
  isAuthenticated: false,
  login: (userData, token) => {},
  logout: () => {},
  updateUser: (userData) => {}
}
```

### Proteção de Rotas (Frontend)
```jsx
// ProtectedRoute.jsx
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuthStore()
  return isAuthenticated ? children : <Navigate to="/login" />
}
```

### Autenticação JWT (Backend)
```python
# auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return username
```

## 📊 Gerenciamento de Estado

### Zustand Stores (Frontend)
```javascript
// cvStore.js
{
  cvs: [],
  currentCv: null,
  analysisHistory: [],
  isLoading: false,
  setCvs: (cvs) => {},
  addCv: (cv) => {},
  setCurrentCv: (cv) => {}
}
```

### Banco de Dados (Backend)
```python
# models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime)

class CV(Base):
    __tablename__ = "cvs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    file_path = Column(String)
    uploaded_at = Column(DateTime)
    analysis_result = Column(Text)
```

## 🌐 API Integration

### Cliente HTTP (Frontend)
```javascript
// api/client.js
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' }
})

// Interceptor para adicionar token
apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

### Endpoints da API (Backend)
```python
# api/cv.py
@app.post("/cv/upload")
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Validação do arquivo
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400, 
                detail="Apenas arquivos PDF são aceitos"
            )
        
        # Processamento do arquivo
        # ... lógica de processamento
        
        return {"message": "CV enviado com sucesso"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Endpoints Principais
- `POST /auth/login` - Login de usuário
- `POST /auth/register` - Registro de usuário
- `POST /cv/upload` - Upload de currículo
- `GET /cv` - Lista de currículos
- `POST /cv/{id}/analyze` - Análise de currículo
- `GET /cv/{id}/analysis` - Resultado da análise

## 🧪 Testes

### Configuração Jest (Frontend)
```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1'
  }
}
```

### Configuração Pytest (Backend)
```python
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### Estrutura de Testes
```
# Frontend
src/
├── __tests__/
│   ├── components/
│   ├── pages/
│   └── utils/
└── setupTests.js

# Backend
tests/
├── test_auth.py
├── test_cv.py
├── test_ai_analysis.py
└── conftest.py
```

## 🚀 Deploy

### Build de Produção (Frontend)
```bash
npm run build
# Gera pasta dist/ com arquivos otimizados
```

### Build de Produção (Backend)
```bash
# Instalar dependências de produção
pip install -r requirements.txt

# Executar com Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Plataformas de Deploy
- **Vercel**: Deploy automático do GitHub (Frontend)
- **Netlify**: Deploy com preview (Frontend)
- **Railway**: Deploy automático (Backend)
- **Heroku**: Deploy com Git (Backend)
- **GitHub Pages**: Deploy gratuito (Frontend)

### Configuração de Deploy
```bash
# Vercel (Frontend)
vercel --prod

# Netlify (Frontend)
netlify deploy --prod

# Railway (Backend)
railway up

# Heroku (Backend)
git push heroku main
```

## 📚 Recursos Adicionais

### Bibliotecas Recomendadas (Frontend)
- **Formulários**: react-hook-form, yup
- **Notificações**: react-hot-toast, react-toastify
- **Gráficos**: recharts, chart.js
- **Upload**: react-dropzone
- **Ícones**: lucide-react, heroicons

### Bibliotecas Recomendadas (Backend)
- **Validação**: pydantic, marshmallow
- **Upload**: python-multipart, aiofiles
- **IA**: openai, google-generativeai, spacy
- **PDF**: PyMuPDF, pdfplumber
- **Testes**: pytest, pytest-asyncio, httpx

### Ferramentas de Desenvolvimento
- **Frontend**: ESLint, Prettier, Husky, Lint-staged
- **Backend**: Black, isort, flake8, mypy
- **Full-stack**: Docker, Docker Compose

## 🔍 Debugging

### Console Logs (Frontend)
```javascript
// Debug de componentes
console.log('Component rendered:', props)

// Debug de estado
console.log('State changed:', state)

// Debug de API
console.log('API response:', response)
```

### Logs (Backend)
```python
# Debug básico
print("Debug info")

# Logging estruturado
import logging
logging.info("Debug info")

# Logs do FastAPI
logger = logging.getLogger(__name__)
logger.info("API endpoint called")
```

### React DevTools
- Instale a extensão no navegador
- Use para inspecionar componentes
- Monitore mudanças de estado

### FastAPI DevTools
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI**: http://localhost:8000/openapi.json

## 📝 Padrões de Código

### Nomenclatura
- **Frontend**: 
  - Componentes: PascalCase (`MeuComponente.jsx`)
  - Arquivos: camelCase (`meuArquivo.js`)
  - Pastas: kebab-case (`minha-pasta/`)
- **Backend**:
  - Funções: snake_case (`minha_funcao`)
  - Classes: PascalCase (`MinhaClasse`)
  - Constantes: UPPER_SNAKE_CASE (`MAX_SIZE`)

### Estrutura de Componentes (Frontend)
```jsx
import React, { useState, useEffect } from 'react'

function MeuComponente({ prop1, prop2 }) {
  // 1. Hooks
  const [estado, setEstado] = useState(initialValue)
  
  // 2. Effects
  useEffect(() => {
    // Lógica do effect
  }, [dependencies])
  
  // 3. Handlers
  const handleClick = () => {
    // Lógica do handler
  }
  
  // 4. Render
  return (
    <div className="container">
      <h1>{prop1}</h1>
      <button onClick={handleClick}>{prop2}</button>
    </div>
  )
}

export default MeuComponente
```

### Estrutura de Endpoints (Backend)
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/cv/upload")
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Validação do arquivo
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400, 
                detail="Apenas arquivos PDF são aceitos"
            )
        
        # Processamento do arquivo
        # ... lógica de processamento
        
        return {"message": "CV enviado com sucesso"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

**Nota**: Esta configuração pode ser ajustada conforme as necessidades do projeto evoluem.
