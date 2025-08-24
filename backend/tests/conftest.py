"""
Configuração e fixtures comuns para os testes.
"""

import pytest
import asyncio
import os
from typing import Generator
from unittest.mock import patch

# Configurar variáveis de ambiente para testes
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configura o ambiente de teste automaticamente."""
    test_env = {
        "ENVIRONMENT": "test",
        "DEBUG": "true",
        "HOST": "127.0.0.1",
        "PORT": "8001",
        "DATABASE_URL": "sqlite+aiosqlite:///./test_otimizador_cv.db",
        "SECRET_KEY": "test-secret-key-for-testing-only-not-for-production",
        "ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
        "GEMINI_API_KEY": "test-gemini-api-key-for-testing",
        "UPLOAD_DIR": "./test_uploads",
        "MAX_FILE_SIZE": "1048576",
        "SPACY_MODEL": "pt_core_news_sm"
    }
    
    with patch.dict(os.environ, test_env, clear=True):
        yield

# Fixtures básicas para testes
@pytest.fixture(scope="session")
def event_loop():
    """Cria um event loop para testes assíncronos."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def sample_curriculum_text() -> str:
    """Retorna um texto de currículo de exemplo para testes."""
    return """
    Desenvolvedor Python com 5 anos de experiência.
    
    EXPERIÊNCIA PROFISSIONAL:
    - Desenvolvi e implementei 3 sistemas web usando Django e React
    - Liderou uma equipe de 4 desenvolvedores
    - Aumentei a performance da aplicação em 40%
    - Reduzi o tempo de deploy de 2 horas para 15 minutos
    - Gerenciou projetos com orçamento de R$ 500.000
    
    TECNOLOGIAS:
    Python, Django, React, PostgreSQL, AWS, Docker
    
    FORMAÇÃO:
    Bacharel em Ciência da Computação - UFMG (2018-2022)
    """

@pytest.fixture
def sample_job_description() -> str:
    """Retorna uma descrição de vaga de exemplo para testes."""
    return "Desenvolvedor Python com experiência em Django, React e AWS"

@pytest.fixture
def empty_text() -> str:
    """Retorna texto vazio para testes de edge cases."""
    return ""

@pytest.fixture
def short_text() -> str:
    """Retorna texto curto para testes."""
    return "Desenvolvedor Python com experiência."
