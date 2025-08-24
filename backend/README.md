# 🚀 Otimizador de Currículos com IA - Backend

Este é o backend da aplicação **"Otimizador de Currículos com IA"**, desenvolvido em FastAPI com Python 3.11.5. Esta plataforma SaaS permite que usuários façam upload de currículos em PDF, recebam análises detalhadas geradas por IA e acompanhem a evolução da qualidade de seus currículos ao longo do tempo.

## 📋 Índice

- [Visão Geral](#-visão-geral-do-projeto)
- [Arquitetura e Tecnologias](#️-arquitetura-e-tecnologias)
- [Funcionalidades](#-funcionalidades-implementadas)
- [Instalação](#️-instalação-e-configuração)
- [Execução](#️-executando-o-projeto)
- [Estrutura](#-estrutura-do-projeto)
- [API Endpoints](#-endpoints-da-api)
- [Testes](#-testes)
- [Deploy](#-deploy)
- [Contribuição](#-contribuição)

## 🎯 Visão Geral do Projeto

O **Otimizador de Currículos com IA** é uma ferramenta de alto impacto que combina:
- **Upload e processamento de PDFs** de currículos
- **Análise inteligente com IA** usando Google Gemini e spaCy
- **Sistema de autenticação seguro** com JWT
- **Histórico de versões** para acompanhar evolução
- **Métricas quantitativas** para análise de progresso
- **Feedback acionável** para melhorias de currículo

## 🐍 Versão do Python

- **Versão Atual**: Python 3.11.5
- **Gerenciador**: UV (Fast Python package installer and resolver)
- **Ambiente Virtual**: `.venv` com Python 3.11.5

## 🏗️ Arquitetura e Tecnologias

### Core Framework
- **FastAPI** - Framework web moderno, rápido e assíncrono
- **Uvicorn** - Servidor ASGI para FastAPI
- **Pydantic** - Validação de dados e serialização
- **Pydantic-Settings** - Gerenciamento de configurações

### Banco de Dados
- **SQLAlchemy 2.0+** - ORM assíncrono com suporte a asyncio
- **Alembic** - Migrações de banco de dados
- **aiosqlite** - Driver assíncrono para SQLite
- **SQLite** - Banco de dados local para desenvolvimento

### Autenticação e Segurança
- **python-jose** - Codificação/decodificação de tokens JWT
- **passlib[bcrypt]** - Hash seguro de senhas com bcrypt
- **python-multipart** - Upload de arquivos

### Processamento de PDF e IA
- **PyMuPDF (fitz)** - Extração rápida de texto de PDFs
- **spaCy** - Processamento de Linguagem Natural (NLP)
- **google-generativeai** - Integração com Google Gemini API
- **agno** - Construção de agentes inteligentes

### Utilitários
- **aiofiles** - Operações assíncronas com arquivos
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## 📋 Funcionalidades Implementadas

### ✅ Estrutura Base
- [x] Configuração assíncrona com FastAPI
- [x] Sistema de configurações com Pydantic-Settings
- [x] Banco de dados SQLite com SQLAlchemy assíncrono
- [x] Estrutura de pastas organizada
- [x] Configuração de ambiente virtual

### 🚧 Em Desenvolvimento
- [ ] Sistema de autenticação JWT completo
- [ ] Histórico de versões
- [ ] Dashboard com métricas
- [ ] API REST completa

### ✅ Funcionalidades de Análise Implementadas
- [x] Upload e processamento de PDFs com pypdf
- [x] Análise de currículos com spaCy (verbos de ação, quantificação)
- [x] Integração com Google Gemini para feedback qualitativo
- [x] Análise de palavras-chave baseada em descrição de vaga
- [x] Sistema de pontuação e classificação automática
- [x] Persistência de resultados no banco de dados

## 🛠️ Instalação e Configuração

### 1. Pré-requisitos
- **Python 3.11.5** (instalado via UV)
- **UV** - Gerenciador de pacotes Python
- **Git** - Controle de versão

### 2. Instalar Python 3.11.5 via UV

```bash
# Instalar a versão específica do Python
uv python install 3.11.5

# Verificar versões instaladas
uv python list
```

### 3. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual com Python 3.11.5
uv venv --python 3.11.5

# Ativar ambiente virtual (Windows)
.\.venv\Scripts\activate

# Ativar ambiente virtual (Linux/macOS)
source .venv/bin/activate
```

### 4. Instalar Dependências

```bash
# Instalar todas as dependências
uv sync

# Ou instalar apenas dependências de produção
uv sync --no-dev
```

### 5. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar variáveis conforme necessário:
# - GEMINI_API_KEY: Sua chave da API Google Gemini
# - SECRET_KEY: Chave secreta para JWT
# - DATABASE_URL: URL do banco SQLite
```

## 🏃‍♂️ Executando o Projeto

### Modo de Desenvolvimento

```bash
# Com UV
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Ou diretamente com Python
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Modo de Produção

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📁 Estrutura do Projeto

```
backend/
├── .venv/                 # Ambiente virtual Python 3.11.5
├── .python-version        # Versão do Python (3.11.5)
├── .env                   # Variáveis de ambiente
├── pyproject.toml         # Configuração do projeto e dependências
├── main.py                # Arquivo principal da aplicação
├── init_db.py             # Script de inicialização do banco
├── test_metrics_api.py    # Testes da API
├── README.md              # Este arquivo
├── uploads/               # Diretório para uploads de PDFs
└── app/                   # Código da aplicação
    ├── __init__.py
    ├── core/              # Configurações centrais
    │   ├── __init__.py
    │   ├── config.py      # Configurações com Pydantic-Settings
    │   ├── database.py    # Configuração do banco SQLAlchemy
    │   ├── logging.py     # Sistema de logging
    │   └── security.py    # Configurações de segurança
    ├── models/            # Modelos SQLAlchemy
    │   ├── __init__.py
    │   ├── curriculum.py  # Modelo de currículo
    │   └── user.py        # Modelo de usuário
    ├── schemas/           # Schemas Pydantic
    │   ├── __init__.py
    │   ├── common.py      # Schemas comuns
    │   ├── curriculum.py  # Schemas de currículo
    │   ├── metrics.py     # Schemas de métricas
    │   └── user.py        # Schemas de usuário
    ├── routers/           # Rotas da API
    │   ├── __init__.py
    │   ├── auth.py        # Rotas de autenticação
    │   ├── curriculum.py  # Rotas de currículo
    │   └── metrics.py     # Rotas de métricas
    └── utils/             # Utilitários
        ├── __init__.py
        └── file_validator.py  # Validação de arquivos
```

## 🛣️ Endpoints da API

### 🔐 Autenticação (`/api/auth`)
| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|---------|
| `POST` | `/register` | Cadastro de usuário | 🚧 Em desenvolvimento |
| `POST` | `/login` | Login de usuário | 🚧 Em desenvolvimento |
| `POST` | `/logout` | Logout de usuário | 🚧 Em desenvolvimento |

### 📄 Currículos (`/api/curriculum`)
| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|---------|
| `POST` | `/upload` | Upload e análise de currículo PDF | ✅ Implementado |
| `GET` | `/list` | Lista de currículos do usuário | ✅ Implementado |
| `GET` | `/{id}` | Detalhes de um currículo | ✅ Implementado |
| `DELETE` | `/{id}` | Remoção de currículo | ✅ Implementado |

### 📊 Métricas (`/api/metrics`)
| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|---------|
| `GET` | `/history` | Histórico de métricas | 🚧 Em desenvolvimento |
| `GET` | `/progress` | Progresso do usuário | 🚧 Em desenvolvimento |
| `GET` | `/analytics` | Análises detalhadas | 🚧 Em desenvolvimento |

### 🏥 Saúde e Informações (`/`)
| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|---------|
| `GET` | `/` | Informações da API | ✅ Implementado |
| `GET` | `/health` | Health check | ✅ Implementado |
| `GET` | `/docs` | Documentação Swagger | ✅ Implementado |
| `GET` | `/redoc` | Documentação ReDoc | ✅ Implementado |

## 🔧 Comandos Úteis

### Gerenciamento de Dependências

```bash
# Adicionar nova dependência
uv add package-name

# Adicionar dependência de desenvolvimento
uv add --dev package-name

# Remover dependência
uv remove package-name

# Atualizar dependências
uv sync --upgrade
```

### Gerenciamento de Python

```bash
# Listar versões instaladas
uv python list

# Instalar nova versão
uv python install 3.12.0

# Usar versão específica
uv python use 3.11.5
```

### Banco de Dados

```bash
# Criar tabelas
python -c "from app.core.database import create_tables; import asyncio; asyncio.run(create_tables())"

# Remover tabelas (cuidado!)
python -c "from app.core.database import drop_tables; import asyncio; asyncio.run(drop_tables())"
```

## 🧪 Testes

```bash
# Executar testes
uv run pytest

# Executar testes com coverage
uv run pytest --cov=.

# Executar testes específicos
uv run pytest tests/test_auth.py
```

## 📊 Monitoramento e Logs

- **FastAPI Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔒 Segurança

- **JWT**: Autenticação baseada em tokens
- **Bcrypt**: Hash seguro de senhas
- **CORS**: Configuração de origens permitidas
- **Rate Limiting**: Proteção contra ataques de força bruta

## 🚀 Deploy

### Docker

```bash
# Build da imagem
docker build -t otimizador-cv-backend .

# Executar container
docker run -p 8000:8000 otimizador-cv-backend
```

### Produção

```bash
# Usar Gunicorn para produção
uv run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🎯 Funcionalidades Planejadas

### 1. Autenticação e Gestão de Usuários
- [ ] Rotas de cadastro e login
- [ ] Sistema JWT para proteção de rotas
- [ ] Gerenciamento de perfis de usuário

### 2. Upload e Análise de Currículo (.pdf)
- [ ] Upload de arquivos PDF
- [ ] Extração de texto com PyMuPDF
- [ ] Análise com spaCy para:
- [ ] Uso de verbos de ação
- [ ] Quantificação de resultados
- [ ] Análise de palavras-chave

### 3. Integração com IA (Google Gemini & Agno)
- [ ] Análise qualitativa de currículos
- [ ] Sugestões personalizadas
- [ ] Feedback acionável

### 4. Histórico de Versões e Resultados
- [ ] Armazenamento de PDFs originais
- [ ] Histórico de análises
- [ ] Comparação entre versões

### 5. Análise de Progresso
- [ ] Métricas quantitativas
- [ ] Gráficos de evolução
- [ ] Relatórios de melhoria

## 🤝 Contribuição

Este projeto é parte do **Desafio Técnico do Time** para desenvolvimento full-stack.

### Processo de Desenvolvimento

1. **Fork do Repositório**: https://github.com/miguelamaral254/otimizador_de_cv_ia
2. **Desenvolvimento em Branches**: 
   - `feat/backend-setup` - Configuração inicial
   - `feat/auth-system` - Sistema de autenticação
   - `feat/pdf-analysis` - Análise de currículos
   - `feat/gemini-integration` - Integração com IA
3. **Commits Frequentes**: Pequenos e com mensagens claras
4. **Pull Request**: Entrega final com resumo e decisões de arquitetura

### Padrões de Código

- **Type Hints**: Uso obrigatório de type hints
- **Docstrings**: Documentação clara de funções e classes
- **Testes**: Cobertura mínima de 80%
- **Formatação**: Black + isort + flake8
- **Type Checking**: MyPy para verificação estática

## 📝 Próximos Passos

1. **Implementar autenticação JWT** completa
2. **Criar sistema de histórico** de versões
3. **Implementar dashboard** com métricas e gráficos
4. **Adicionar testes unitários** e de integração
5. **Configurar CI/CD** para deploy automático

## 🧪 Testando a Funcionalidade

### Teste das Funções de Análise
```bash
# Execute o teste das funções de análise
python test_analysis.py
```

### Teste da API Completa
```bash
# Inicie o servidor
uv run uvicorn main:app --reload

# Acesse a documentação
# http://localhost:8000/docs
```

### Endpoint de Upload Testado
- **POST** `/api/curriculum/upload` - Upload e análise completa de currículos
- Suporte a arquivos PDF até 10MB
- Análise automática com spaCy e Google Gemini
- Persistência de resultados no banco de dados

## 📄 Licença

Este projeto é parte do desafio técnico do time de desenvolvimento.

---

**Bom trabalho, time! Este é um projeto desafiador e uma ótima oportunidade para construirmos algo incrível juntos.** 🚀
