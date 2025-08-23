from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from app.core.config import settings

# Base para os modelos SQLAlchemy
Base = declarative_base()

# Configuração da engine assíncrona
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    poolclass=StaticPool,  # Para SQLite
    connect_args={"check_same_thread": False},  # Necessário para SQLite
)

# Sessão assíncrona
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """Dependency para obter sessão do banco de dados."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    """Criar todas as tabelas do banco de dados."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """Remover todas as tabelas do banco de dados."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
