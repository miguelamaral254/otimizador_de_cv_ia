"""
Interfaces base para inversão de dependência e segregação de responsabilidades.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from app.schemas.curriculum import CurriculumCreate, CurriculumUpdate, CurriculumResponse


class ICurriculumRepository(ABC):
    """Interface para repositório de currículos."""
    
    @abstractmethod
    async def create(self, curriculum: CurriculumCreate) -> CurriculumResponse:
        """Cria um novo currículo."""
        pass
    
    @abstractmethod
    async def get_by_id(self, curriculum_id: int) -> Optional[CurriculumResponse]:
        """Busca um currículo por ID."""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[CurriculumResponse]:
        """Lista todos os currículos."""
        pass
    
    @abstractmethod
    async def update(self, curriculum_id: int, curriculum: CurriculumUpdate) -> Optional[CurriculumResponse]:
        """Atualiza um currículo."""
        pass
    
    @abstractmethod
    async def delete(self, curriculum_id: int) -> bool:
        """Remove um currículo."""
        pass


class ICurriculumService(ABC):
    """Interface para serviço de currículos."""
    
    @abstractmethod
    async def create_curriculum(self, curriculum: CurriculumCreate) -> CurriculumResponse:
        """Cria um novo currículo."""
        pass
    
    @abstractmethod
    async def get_curriculum(self, curriculum_id: int) -> CurriculumResponse:
        """Busca um currículo por ID."""
        pass
    
    @abstractmethod
    async def list_curriculums(self, skip: int = 0, limit: int = 100) -> List[CurriculumResponse]:
        """Lista todos os currículos."""
        pass
    
    @abstractmethod
    async def update_curriculum(self, curriculum_id: int, curriculum: CurriculumUpdate) -> CurriculumResponse:
        """Atualiza um currículo."""
        pass
    
    @abstractmethod
    async def delete_curriculum(self, curriculum_id: int) -> bool:
        """Remove um currículo."""
        pass


class IAnalysisEngine(ABC):
    """Interface para motor de análise."""
    
    @abstractmethod
    async def analyze_curriculum(self, text: str) -> Dict[str, Any]:
        """Analisa um currículo."""
        pass
    
    @abstractmethod
    async def analyze_quantification(self, text: str) -> Dict[str, Any]:
        """Analisa quantificação no texto."""
        pass
    
    @abstractmethod
    async def analyze_action_verbs(self, text: str) -> Dict[str, Any]:
        """Analisa verbos de ação no texto."""
        pass


class IFileProcessor(ABC):
    """Interface para processamento de arquivos."""
    
    @abstractmethod
    async def process_file(self, file_path: str) -> str:
        """Processa um arquivo e retorna o conteúdo."""
        pass
    
    @abstractmethod
    async def validate_file(self, file_path: str) -> bool:
        """Valida se um arquivo pode ser processado."""
        pass
