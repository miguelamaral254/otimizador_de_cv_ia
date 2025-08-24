from pydantic_settings import BaseSettings, SettingsConfigDict
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
    database_url: str
    
    # Configurações de Segurança
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configurações de IA (Google Gemini)
    gemini_api_key: Optional[str] = None
    
    # Configurações de Upload
    upload_dir: str = "./uploads"
    max_file_size: int = 10485760  # 10MB em bytes
    
    # Configurações de spaCy
    spacy_model: str = "pt_core_news_sm"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Instância global das configurações
settings = Settings()
