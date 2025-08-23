import uuid
import aiofiles
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import fitz  # PyMuPDF para manipulação de PDFs
from datetime import datetime

from app.models.user import User
from app.models.curriculum import Curriculum, CurriculumVersion, CurriculumAnalysis
from app.schemas.curriculum import (
    CurriculumResponse,
    CurriculumUploadResponse,
    CurriculumAnalysisResponse,
)
from app.core.database import get_db
from app.core import settings
from app.api.dependencies import get_current_user

router = APIRouter()


@router.post("/upload", response_model=CurriculumUploadResponse)
async def upload_curriculum(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload de currículo em PDF para análise.

    Args:
        file: Arquivo PDF do currículo
        current_user: Usuário autenticado
        db: Sessão do banco de dados

    Returns:
        CurriculumUploadResponse: Resposta com dados do currículo enviado
    """
    # 1. Validação do arquivo
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas arquivos PDF são aceitos",
        )

    if file.size > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Arquivo muito grande. Tamanho máximo: {settings.max_file_size / 1024 / 1024:.1f}MB",
        )

    # 2. Define o diretório e garante que ele exista
    UPLOAD_DIRECTORY = Path(settings.upload_dir)
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

    # 3. Gera um nome de arquivo único e seguro
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIRECTORY / unique_filename

    try:
        # 4. Lê o conteúdo do arquivo e salva no diretório
        contents = await file.read()
        async with aiofiles.open(file_path, "wb") as buffer:
            await buffer.write(contents)

        # 5. Extrai o texto do PDF
        extracted_text = ""
        try:
            with fitz.open(file_path) as doc:
                for page in doc:
                    extracted_text += page.get_text()
        except Exception as e:
            # Remove o arquivo se houver erro no processamento
            file_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao processar o PDF: {str(e)}",
            )

        # 6. Salva informações no banco de dados
        new_curriculum = Curriculum(
            user_id=current_user.id,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=file.size,
            title=file.filename.replace(".pdf", ""),
            description=f"Currículo enviado em {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        )

        db.add(new_curriculum)
        await db.commit()
        await db.refresh(new_curriculum)

        # 7. Retorna resposta de sucesso
        return CurriculumUploadResponse(
            curriculum=CurriculumResponse(
                id=new_curriculum.id,
                user_id=new_curriculum.user_id,
                original_filename=new_curriculum.original_filename,
                file_path=new_curriculum.file_path,
                file_size=new_curriculum.file_size,
                created_at=new_curriculum.created_at,
                updated_at=new_curriculum.updated_at,
            ),
            message="Currículo enviado com sucesso!",
        )

    except Exception as e:
        # Remove o arquivo em caso de erro
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}",
        )


@router.get("/history", response_model=list[CurriculumResponse])
async def get_history(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    Obtém o histórico de currículos do usuário.

    Args:
        current_user: Usuário autenticado
        db: Sessão do banco de dados

    Returns:
        List[CurriculumResponse]: Lista de currículos do usuário
    """
    try:
        result = await db.execute(
            select(Curriculum).where(Curriculum.user_id == current_user.id)
        )
        curricula = result.scalars().all()

        return [
            CurriculumResponse(
                id=curriculum.id,
                user_id=curriculum.user_id,
                original_filename=curriculum.original_filename,
                file_path=curriculum.file_path,
                file_size=curriculum.file_size,
                created_at=curriculum.created_at,
                updated_at=curriculum.updated_at,
            )
            for curriculum in curricula
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar histórico: {str(e)}",
        )


@router.get("/{curriculum_id}", response_model=CurriculumResponse)
async def get_curriculum(
    curriculum_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Obtém um currículo específico do usuário.

    Args:
        curriculum_id: ID do currículo
        current_user: Usuário autenticado
        db: Sessão do banco de dados

    Returns:
        CurriculumResponse: Dados do currículo
    """
    try:
        result = await db.execute(
            select(Curriculum).where(
                Curriculum.id == curriculum_id, Curriculum.user_id == current_user.id
            )
        )
        curriculum = result.scalar_one_or_none()

        if not curriculum:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Currículo não encontrado"
            )

        return CurriculumResponse(
            id=curriculum.id,
            user_id=curriculum.user_id,
            original_filename=curriculum.original_filename,
            file_path=curriculum.file_path,
            file_size=curriculum.file_size,
            created_at=curriculum.created_at,
            updated_at=curriculum.updated_at,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}",
        )


@router.get(
    "/{curriculum_id}/analyses", response_model=list[CurriculumAnalysisResponse]
)
async def get_curriculum_analyses(
    curriculum_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Obtém todas as análises de um currículo específico do usuário.

    Args:
        curriculum_id: ID do currículo
        current_user: Usuário autenticado
        db: Sessão do banco de dados

    Returns:
        List[CurriculumAnalysisResponse]: Lista de análises do currículo
    """
    try:
        # Verificar se o currículo pertence ao usuário
        curriculum_result = await db.execute(
            select(Curriculum).where(
                Curriculum.id == curriculum_id, Curriculum.user_id == current_user.id
            )
        )
        curriculum = curriculum_result.scalar_one_or_none()

        if not curriculum:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Currículo não encontrado"
            )

        # Buscar todas as análises do currículo
        analyses_result = await db.execute(
            select(CurriculumAnalysis)
            .where(CurriculumAnalysis.curriculum_id == curriculum_id)
            .order_by(CurriculumAnalysis.analysis_date)
        )
        analyses = analyses_result.scalars().all()

        return [
            CurriculumAnalysisResponse(
                id=analysis.id,
                curriculum_id=analysis.curriculum_id,
                version_id=analysis.version_id,
                spacy_analysis=analysis.spacy_analysis,
                gemini_analysis=analysis.gemini_analysis,
                action_verbs_count=analysis.action_verbs_count,
                quantified_results_count=analysis.quantified_results_count,
                keywords_score=analysis.keywords_score,
                overall_score=analysis.overall_score,
                strengths=analysis.strengths or [],
                weaknesses=analysis.weaknesses or [],
                suggestions=analysis.suggestions or [],
                analysis_date=analysis.analysis_date,
                processing_time=analysis.processing_time,
            )
            for analysis in analyses
        ]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}",
        )
