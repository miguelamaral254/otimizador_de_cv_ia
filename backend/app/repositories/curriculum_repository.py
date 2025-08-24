"""
Implementação concreta do repositório de currículos.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.core.interfaces import ICurriculumRepository
from app.models.curriculum import Curriculum
from app.schemas.curriculum import CurriculumCreate, CurriculumUpdate, CurriculumResponse


class CurriculumRepository(ICurriculumRepository):
    """Implementação concreta do repositório de currículos."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, curriculum: CurriculumCreate) -> CurriculumResponse:
        """Cria um novo currículo."""
        db_curriculum = Curriculum(**curriculum.dict())
        self.db.add(db_curriculum)
        await self.db.commit()
        await self.db.refresh(db_curriculum)
        return CurriculumResponse.from_orm(db_curriculum)
    
    async def get_by_id(self, curriculum_id: int) -> Optional[CurriculumResponse]:
        """Busca um currículo por ID."""
        result = await self.db.execute(
            select(Curriculum).where(Curriculum.id == curriculum_id)
        )
        db_curriculum = result.scalar_one_or_none()
        return CurriculumResponse.from_orm(db_curriculum) if db_curriculum else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[CurriculumResponse]:
        """Lista todos os currículos."""
        result = await self.db.execute(
            select(Curriculum).offset(skip).limit(limit)
        )
        curriculums = result.scalars().all()
        return [CurriculumResponse.from_orm(curriculum) for curriculum in curriculums]
    
    async def update(self, curriculum_id: int, curriculum: CurriculumUpdate) -> Optional[CurriculumResponse]:
        """Atualiza um currículo."""
        update_data = curriculum.dict(exclude_unset=True)
        result = await self.db.execute(
            update(Curriculum)
            .where(Curriculum.id == curriculum_id)
            .values(**update_data)
        )
        
        if result.rowcount == 0:
            return None
            
        await self.db.commit()
        return await self.get_by_id(curriculum_id)
    
    async def delete(self, curriculum_id: int) -> bool:
        """Remove um currículo."""
        result = await self.db.execute(
            delete(Curriculum).where(Curriculum.id == curriculum_id)
        )
        await self.db.commit()
        return result.rowcount > 0
