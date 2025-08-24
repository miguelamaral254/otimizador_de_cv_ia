"""
Factory para gerenciar injeção de dependências.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.interfaces import ICurriculumRepository, ICurriculumService, IAnalysisEngine
from app.repositories.curriculum_repository import CurriculumRepository
from app.services.curriculum_service import CurriculumService
from otimizador_de_cv_ia.backend.app.agno.analysis_engine import RefactoredAnalysisEngine


class ServiceFactory:
    """Factory para criar instâncias de serviços."""
    
    def __init__(self):
        self._analysis_engine: Optional[IAnalysisEngine] = None
        self._curriculum_repository: Optional[ICurriculumRepository] = None
        self._curriculum_service: Optional[ICurriculumService] = None
    
    def get_analysis_engine(self) -> IAnalysisEngine:
        """Retorna uma instância do motor de análise."""
        if not self._analysis_engine:
            self._analysis_engine = RefactoredAnalysisEngine()
        return self._analysis_engine
    
    def get_curriculum_repository(self, db: AsyncSession) -> ICurriculumRepository:
        """Retorna uma instância do repositório de currículos."""
        if not self._curriculum_repository:
            self._curriculum_repository = CurriculumRepository(db)
        return self._curriculum_repository
    
    def get_curriculum_service(self, db: AsyncSession) -> ICurriculumService:
        """Retorna uma instância do serviço de currículos."""
        if not self._curriculum_service:
            repository = self.get_curriculum_repository(db)
            analysis_engine = self.get_analysis_engine()
            self._curriculum_service = CurriculumService(repository, analysis_engine)
        return self._curriculum_service
    
    def reset(self):
        """Reseta todas as instâncias (útil para testes)."""
        self._analysis_engine = None
        self._curriculum_repository = None
        self._curriculum_service = None


# Instância global do factory
service_factory = ServiceFactory()


def get_curriculum_service(db: AsyncSession) -> ICurriculumService:
    """Dependency injection para o serviço de currículos."""
    return service_factory.get_curriculum_service(db)


def get_analysis_engine() -> IAnalysisEngine:
    """Dependency injection para o motor de análise."""
    return service_factory.get_analysis_engine()
