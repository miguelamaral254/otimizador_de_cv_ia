"""
Configuração e fixtures comuns para os testes.
"""

import pytest
import asyncio
from typing import Generator

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
