"""
Serviço de currículos implementando a lógica de negócio.
"""

from typing import List, Optional
from app.core.interfaces import ICurriculumRepository, ICurriculumService, IAnalysisEngine
from app.schemas.curriculum import CurriculumCreate, CurriculumUpdate, CurriculumResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


class CurriculumService(ICurriculumService):
    """Serviço de currículos implementando a lógica de negócio."""
    
    def __init__(
        self, 
        repository: ICurriculumRepository,
        analysis_engine: IAnalysisEngine
    ):
        self.repository = repository
        self.analysis_engine = analysis_engine
    
    async def create_curriculum(self, curriculum: CurriculumCreate) -> CurriculumResponse:
        """Cria um novo currículo com análise automática."""
        try:
            # Cria o currículo no banco
            db_curriculum = await self.repository.create(curriculum)
            
            # Analisa o currículo se houver arquivo
            if hasattr(curriculum, 'file_path') and curriculum.file_path:
                # Aqui você pode implementar a leitura do arquivo para análise
                # Por enquanto, vamos apenas logar
                logger.info(f"Currículo {db_curriculum.id} criado com sucesso")
            
            return db_curriculum
            
        except Exception as e:
            logger.error(f"Erro ao criar currículo: {e}")
            raise
    
    async def get_curriculum(self, curriculum_id: int) -> CurriculumResponse:
        """Busca um currículo por ID."""
        curriculum = await self.repository.get_by_id(curriculum_id)
        if not curriculum:
            raise ValueError(f"Currículo com ID {curriculum_id} não encontrado")
        return curriculum
    
    async def list_curriculums(self, skip: int = 0, limit: int = 100) -> List[CurriculumResponse]:
        """Lista todos os currículos."""
        return await self.repository.get_all(skip=skip, limit=limit)
    
    async def update_curriculum(self, curriculum_id: int, curriculum: CurriculumUpdate) -> CurriculumResponse:
        """Atualiza um currículo."""
        updated = await self.repository.update(curriculum_id, curriculum)
        if not updated:
            raise ValueError(f"Currículo com ID {curriculum_id} não encontrado")
        return updated
    
    async def delete_curriculum(self, curriculum_id: int) -> bool:
        """Remove um currículo."""
        return await self.repository.delete(curriculum_id)
    
    async def analyze_curriculum_content(self, curriculum_id: int) -> dict:
        """Analisa o conteúdo de um currículo específico."""
        curriculum = await self.get_curriculum(curriculum_id)
        if not curriculum.file_path:
            raise ValueError("Currículo não possui arquivo para análise")
        
        # Aqui você pode implementar a leitura do arquivo
        # Por enquanto, vamos retornar uma análise mock
        return await self.analysis_engine.analyze_curriculum("Conteúdo do currículo")
