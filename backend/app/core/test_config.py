"""
Configuração específica para testes.
"""

from typing import Generator
from unittest.mock import Mock, AsyncMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# from app.main import app  # Comentado para evitar import circular
from app.core.database import get_db, Base
from app.core.interfaces import ICurriculumRepository, ICurriculumService, IAnalysisEngine


# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override da dependência de banco para testes."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Mock do repositório para testes
class MockCurriculumRepository(ICurriculumRepository):
    """Mock do repositório para testes."""
    
    def __init__(self):
        self.curriculums = {}
        self.next_id = 1
    
    async def create(self, curriculum):
        curriculum_id = self.next_id
        self.next_id += 1
        self.curriculums[curriculum_id] = curriculum
        return curriculum
    
    async def get_by_id(self, curriculum_id):
        return self.curriculums.get(curriculum_id)
    
    async def get_all(self, skip=0, limit=100):
        items = list(self.curriculums.values())
        return items[skip:skip + limit]
    
    async def update(self, curriculum_id, curriculum):
        if curriculum_id in self.curriculums:
            self.curriculums[curriculum_id] = curriculum
            return curriculum
        return None
    
    async def delete(self, curriculum_id):
        if curriculum_id in self.curriculums:
            del self.curriculums[curriculum_id]
            return True
        return False


# Mock do motor de análise para testes
class MockAnalysisEngine(IAnalysisEngine):
    """Mock do motor de análise para testes."""
    
    async def analyze_curriculum(self, text):
        return {
            'quantification': {'score': 7.5, 'numbers': ['5', '25%']},
            'action_verbs': {'score': 8.0, 'total_verbs': 4},
            'keywords': {'score': 6.5, 'total_keywords': 3},
            'total_score': 7.3,
            'overall_assessment': 'good'
        }
    
    async def analyze_quantification(self, text):
        return {'score': 7.5, 'numbers': ['5', '25%']}
    
    async def analyze_action_verbs(self, text):
        return {'score': 8.0, 'total_verbs': 4}


# Mock do serviço para testes
class MockCurriculumService(ICurriculumService):
    """Mock do serviço para testes."""
    
    def __init__(self):
        self.repository = MockCurriculumRepository()
        self.analysis_engine = MockAnalysisEngine()
    
    async def create_curriculum(self, curriculum):
        return await self.repository.create(curriculum)
    
    async def get_curriculum(self, curriculum_id):
        curriculum = await self.repository.get_by_id(curriculum_id)
        if not curriculum:
            raise ValueError(f"Currículo com ID {curriculum_id} não encontrado")
        return curriculum
    
    async def list_curriculums(self, skip=0, limit=100):
        return await self.repository.get_all(skip=skip, limit=limit)
    
    async def update_curriculum(self, curriculum_id, curriculum):
        updated = await self.repository.update(curriculum_id, curriculum)
        if not updated:
            raise ValueError(f"Currículo com ID {curriculum_id} não encontrado")
        return updated
    
    async def delete_curriculum(self, curriculum_id):
        return await self.repository.delete(curriculum_id)
    
    async def analyze_curriculum_content(self, curriculum_id):
        return await self.analysis_engine.analyze_curriculum("Texto de teste")


# Funções de configuração para testes
def get_test_client() -> TestClient:
    """Retorna um cliente de teste configurado."""
    # Import local para evitar import circular
    from app.main import app
    return TestClient(app)


def setup_test_database():
    """Configura o banco de dados de teste."""
    Base.metadata.create_all(bind=engine)


def teardown_test_database():
    """Limpa o banco de dados de teste."""
    Base.metadata.drop_all(bind=engine)


def get_mock_curriculum_service() -> ICurriculumService:
    """Retorna um serviço mock para testes."""
    return MockCurriculumService()


def get_mock_analysis_engine() -> IAnalysisEngine:
    """Retorna um motor de análise mock para testes."""
    return MockAnalysisEngine()


def get_mock_curriculum_repository() -> ICurriculumRepository:
    """Retorna um repositório mock para testes."""
    return MockCurriculumRepository()
