# 🚀 Frontend - Otimizador de Currículos com IA

Este é o **frontend React** da aplicação "Otimizador de Currículos com IA", uma plataforma SaaS completa para análise e otimização de currículos usando inteligência artificial.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Arquitetura](#️-arquitetura-do-projeto)
- [Setup](#️-setup-inicial)
- [Estrutura](#-estrutura-do-frontend)
- [Tecnologias](#-tecnologias-configuradas)
- [Funcionalidades](#-funcionalidades)
- [Desenvolvimento](#-comandos-úteis-para-desenvolvimento)
- [Recursos](#-recursos-de-aprendizado)
- [Entrega](#-entrega-final)

## 🎯 Objetivo do Desafio

Construir uma **aplicação web full-stack completa** para otimização de currículos usando inteligência artificial, incluindo:

### Frontend (React)
- Sistema de upload de arquivos PDF
- Dashboard com métricas e visualizações
- Sistema de autenticação
- Histórico de versões

### Backend (FastAPI + Python)
- API REST completa com FastAPI
- Sistema de autenticação JWT
- Processamento de PDFs com PyMuPDF
- Análise de IA com Google Gemini e spaCy
- Banco de dados SQLite com SQLAlchemy

## 🏗️ Arquitetura do Projeto

```
otimizador_de_cv_ia/
├── frontend/                 # Frontend React (este diretório)
│   ├── src/
│   │   ├── components/      # Componentes reutilizáveis
│   │   ├── pages/           # Páginas da aplicação
│   │   ├── App.jsx          # Componente principal
│   │   ├── main.jsx         # Ponto de entrada
│   │   └── index.css        # Estilos globais
│   ├── package.json         # Dependências Node.js
│   └── README.md            # Este arquivo
└── backend/                  # Backend FastAPI (Python)
    ├── app/                  # Código da aplicação
    ├── main.py              # Ponto de entrada
    ├── pyproject.toml       # Dependências Python
    └── README.md            # Documentação do backend
```

## 🛠️ Setup Inicial

### Pré-requisitos
- **Node.js 18+** - [Download aqui](https://nodejs.org/)
- **Python 3.11.5+** - [Download aqui](https://www.python.org/)
- **npm ou yarn** - Gerenciador de pacotes
- **Git** - Controle de versão

### 🚀 Primeiros Passos

1. **Clone o repositório**
   ```bash
   git clone https://github.com/miguelamaral254/otimizador_de_cv_ia.git
   cd otimizador_de_cv_ia
   ```

2. **Setup do Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   A aplicação estará disponível em `http://localhost:3000`

3. **Setup do Backend**
   ```bash
   cd ../backend
   # Criar ambiente virtual Python
   python -m venv .venv
   
   # Ativar ambiente virtual (Windows)
   .\.venv\Scripts\activate
   
   # Ativar ambiente virtual (Linux/macOS)
   source .venv/bin/activate
   
   # Instalar dependências
   pip install -r requirements.txt
   
   # Executar servidor
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   A API estará disponível em `http://localhost:8000`

## 📁 Estrutura do Frontend

```
src/
├── components/          # Componentes reutilizáveis
│   ├── Header.jsx      # Cabeçalho da aplicação
│   └── Footer.jsx      # Rodapé da aplicação
├── pages/               # Páginas da aplicação
│   ├── Home.jsx        # Página inicial
│   ├── About.jsx       # Sobre o projeto
│   └── Contact.jsx     # Página de contato
├── api/                 # Cliente HTTP e configurações
│   ├── auth.js         # API de autenticação
│   └── client.js       # Cliente Axios configurado
├── App.jsx              # Componente principal
├── main.jsx            # Ponto de entrada
└── index.css           # Estilos globais
```

## 🎨 Design System

### Cores
- **Primária**: Azul (#3B82F6)
- **Secundária**: Verde (#10B981)
- **Aviso**: Amarelo (#F59E0B)
- **Erro**: Vermelho (#EF4444)
- **Neutro**: Cinza (#6B7280)

### Tipografia
- **Títulos**: Inter, sans-serif
- **Corpo**: Inter, sans-serif
- **Monospace**: JetBrains Mono

### Componentes
- Botões com estados hover/focus
- Cards com sombras sutis
- Formulários com validação visual
- Modais responsivos

### Responsividade
- **Mobile First**: Design otimizado para dispositivos móveis
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)
- **Grid System**: Flexbox e CSS Grid
- **Touch Friendly**: Elementos otimizados para toque

## 🔧 Scripts Disponíveis

```bash
# Desenvolvimento
npm run dev          # Inicia servidor de desenvolvimento
npm run build        # Gera build de produção
npm run preview      # Visualiza build de produção
npm run lint         # Executa linter

# Alternativas com yarn
yarn dev
yarn build
yarn preview
yarn lint
```

## 🎨 Tecnologias Configuradas

### Frontend
- **React 18.2.0** - Biblioteca principal
- **React Router DOM 6.20.1** - Roteamento
- **Tailwind CSS 3.3.6** - Framework CSS
- **Vite 5.0.0** - Build tool
- **ESLint** - Linting de código

### Backend (FastAPI)
- **Python 3.11.5** - Linguagem principal
- **FastAPI** - Framework web moderno
- **SQLAlchemy 2.0+** - ORM assíncrono
- **PyMuPDF** - Processamento de PDFs
- **spaCy** - Processamento de linguagem natural
- **Google Gemini** - API de IA
- **JWT** - Autenticação segura

## 📋 Funcionalidades

### ✅ Implementadas
- [x] **Estrutura Base React**
  - Setup do projeto com Vite
  - Roteamento com React Router
  - Configuração Tailwind CSS
  - Componentes base (Header, Footer)
  - Páginas principais (Home, About, Contact)

- [x] **Configuração de Build**
  - Sistema de build com Vite
  - Configuração ESLint
  - PostCSS e Autoprefixer
  - Build de produção otimizado

- [x] **Cliente HTTP**
  - Configuração Axios
  - Interceptors para autenticação
  - Tratamento de erros centralizado

### 🚧 Em Desenvolvimento
- [ ] **Sistema de Autenticação**
  - Páginas de Login/Register
  - Gerenciamento de estado com Zustand
  - Proteção de rotas
  - Persistência de sessão

- [ ] **Dashboard Principal**
  - Upload de currículos com drag & drop
  - Visualização de métricas
  - Histórico de análises
  - Gráficos de progresso

- [ ] **Sistema de Upload**
  - Componente React Dropzone
  - Validação de arquivos PDF
  - Barra de progresso
  - Tratamento de erros

### 📋 Planejadas
- [ ] **Análise de Currículos**
  - Visualização de resultados de IA
  - Comparação entre versões
  - Sugestões de melhoria
  - Exportação de relatórios

- [ ] **Funcionalidades Avançadas**
  - Sistema de notificações
  - Filtros e busca avançada
  - Responsividade mobile completa
  - PWA (Progressive Web App)

## 🚀 Comandos Úteis para Desenvolvimento

### Git Workflow
```bash
# Criar nova branch para feature
git checkout -b feat/nome-da-feature

# Ver status das mudanças
git status

# Adicionar mudanças
git add .

# Fazer commit
git commit -m "feat: implementa sistema de upload"

# Enviar para repositório remoto
git push origin feat/nome-da-feature
```

### Frontend (React)
```bash
# Instalar nova dependência
npm install nome-do-pacote
npm install -D nome-do-pacote-dev

# Remover dependência
npm uninstall nome-do-pacote

# Ver dependências desatualizadas
npm outdated

# Atualizar dependências
npm update
```

### Backend (Python)
```bash
# Ativar ambiente virtual
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\activate   # Windows

# Instalar dependência
pip install nome-do-pacote

# Gerar requirements.txt
pip freeze > requirements.txt

# Executar servidor
uvicorn main:app --reload --port 8000
```

### Debugging
```bash
# Frontend - DevTools do navegador
F12 ou Ctrl+Shift+I

# Frontend - Console do navegador
console.log('Debug info')

# Backend - Logs do servidor
print("Debug info")  # Python
logging.info("Debug info")  # Logging estruturado
```

## 📚 Recursos de Aprendizado

### Frontend
- [React](https://react.dev/) - Documentação oficial
- [React Router](https://reactrouter.com/) - Roteamento
- [Tailwind CSS](https://tailwindcss.com/docs) - Framework CSS
- [Vite](https://vitejs.dev/) - Build tool

### Backend
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web
- [SQLAlchemy](https://docs.sqlalchemy.org/) - ORM
- [PyMuPDF](https://pymupdf.readthedocs.io/) - Processamento de PDFs
- [spaCy](https://spacy.io/) - Processamento de linguagem natural
- [Google Gemini](https://ai.google.dev/) - API de IA

### APIs de IA
- [OpenAI API](https://platform.openai.com/docs)
- [Google Gemini](https://ai.google.dev/)
- [Hugging Face](https://huggingface.co/)

## 🔍 Dicas de Desenvolvimento

### Estrutura de Componentes (Frontend)
```jsx
// Componente funcional básico
function MeuComponente({ prop1, prop2 }) {
  const [estado, setEstado] = useState(initialValue)
  
  const handleClick = () => {
    // Lógica do componente
  }
  
  return (
    <div className="container">
      <h1>{prop1}</h1>
      <button onClick={handleClick}>{prop2}</button>
    </div>
  )
}
```

### Estrutura de API (Backend)
```python
# Endpoint básico
@app.post("/cv/upload")
async def upload_cv(file: UploadFile):
    # Validação do arquivo
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas PDFs são aceitos")
    
    # Processamento do arquivo
    content = await file.read()
    # ... lógica de processamento
    
    return {"message": "CV enviado com sucesso"}
```

### Estilização com Tailwind
```jsx
// Classes utilitárias
<div className="
  bg-white 
  rounded-lg 
  shadow-md 
  p-6 
  hover:shadow-lg 
  transition-shadow
">
  Conteúdo do card
</div>
```

## 🐛 Solução de Problemas

### Frontend
```bash
# Erro: "Module not found"
rm -rf node_modules package-lock.json
npm install

# Erro: "Port already in use"
npx kill-port 3000

# Erro: "Tailwind classes not working"
npx tailwindcss init
```

### Backend
```bash
# Erro: "Module not found"
pip install -r requirements.txt

# Erro: "Port already in use"
npx kill-port 8000

# Erro: "Environment not activated"
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\activate   # Windows
```

## 📝 Padrões de Código

### Nomenclatura
- **Componentes**: PascalCase (`MeuComponente.jsx`)
- **Arquivos**: camelCase (`meuArquivo.js`)
- **Pastas**: kebab-case (`minha-pasta/`)
- **Python**: snake_case (`minha_funcao`)

### Estrutura de Commits
```bash
feat: nova funcionalidade
fix: correção de bug
docs: documentação
style: formatação
refactor: refatoração
test: testes
chore: tarefas de manutenção
```

## 🎉 Entrega Final

### Checklist de Entrega
- [ ] Frontend funcional com todas as funcionalidades
- [ ] Backend com API completa e funcional
- [ ] Integração frontend-backend funcionando
- [ ] Sistema de IA implementado e funcionando
- [ ] Código limpo e bem documentado
- [ ] Responsividade mobile
- [ ] Testes básicos
- [ ] README atualizado
- [ ] Deploy funcionando

### Como Entregar
1. Faça commit de todas as mudanças
2. Crie um Pull Request para a branch main
3. Inclua screenshots da aplicação funcionando
4. Documente as decisões técnicas tomadas
5. Inclua instruções de setup e execução

## 🤝 Suporte

- **Issues**: [GitHub Issues](https://github.com/miguelamaral254/otimizador_de_cv_ia/issues)
- **Discussions**: [GitHub Discussions](https://github.com/miguelamaral254/otimizador_de_cv_ia/discussions)
- **Wiki**: [Documentação do Projeto](https://github.com/miguelamaral254/otimizador_de_cv_ia/wiki)

## 🔗 Links Úteis

- **Repositório Principal**: https://github.com/miguelamaral254/otimizador_de_cv_ia
- **Backend README**: [../backend/README.md](../backend/README.md)
- **Documentação FastAPI**: https://fastapi.tiangolo.com/
- **Documentação React**: https://react.dev/

---

**Boa sorte no desafio! 🚀**

*Lembre-se: O objetivo é aprender e crescer como desenvolvedor full-stack. 
Não tenha medo de experimentar e errar!*
