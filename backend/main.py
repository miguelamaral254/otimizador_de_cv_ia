from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.routers import curriculum, auth, metrics
from app.core.database import create_tables

# Configura logging
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciador de ciclo de vida da aplicação."""
    # Startup
    logger.info("🚀 Iniciando Otimizador de Currículos com IA...")
    try:
        await create_tables()
        logger.info("✅ Banco de dados inicializado")
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar banco de dados: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Encerrando aplicação...")


# Criação da aplicação FastAPI
app = FastAPI(
    title="Otimizador de Currículos com IA",
    description="API para análise e otimização de currículos usando IA",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Middlewares de segurança
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["https://seu-dominio.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else ["seu-dominio.com"]
)

# Registro das rotas
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["authentication"]
)

app.include_router(
    curriculum.router,
    prefix="/api/v1/curriculum",
    tags=["curriculum"]
)

app.include_router(
    metrics.router,
    prefix="/api/v1/metrics",
    tags=["metrics"]
)

# Rota de health check
@app.get("/health", tags=["health"])
async def health_check():
    """Verificação de saúde da aplicação."""
    logger.info("Health check solicitado")
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.environment
    }

# Rota raiz
@app.get("/", tags=["root"])
async def root():
    """Rota raiz da aplicação."""
    logger.info("Acesso à rota raiz")
    return {
        "message": "Bem-vindo ao Otimizador de Currículos com IA!",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    # Configura logging antes de iniciar
    setup_logging()
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )