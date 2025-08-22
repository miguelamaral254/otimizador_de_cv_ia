import os

# Chave secreta (gerar uma segura)
SECRET_KEY = os.getenv("SECRET_KEY", "sua_chave_super_secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # tempo em minutos
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configurações da aplicação usando Pydantic Settings."""
    
    # Configurações do Backend
    environment: str = "development"
    debug: bool = True
    
    # Configurações do Servidor
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Configurações de Banco de Dados
    database_url: str = "sqlite+aiosqlite:///./otimizador_cv.db"
    
    # Configurações de Segurança
    secret_key: str = "your-secret-key-here-change-in-production-make-it-very-long-and-random"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configurações de IA (Google Gemini)
    gemini_api_key: Optional[str] = None
    
    # Configurações de Upload
    upload_dir: str = "./uploads"
    max_file_size: int = 10485760  # 10MB em bytes
    
    # Configurações de spaCy
    spacy_model: str = "pt_core_news_sm"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Instância global das configurações
settings = Settings()
