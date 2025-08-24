"""
Router de currículos refatorado seguindo princípios SOLID.
"""

import json
import os
import uuid
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.interfaces import ICurriculumService
from app.services.curriculum_service import CurriculumService
from app.repositories.curriculum_repository import CurriculumRepository
from app.agno import (
    analisar_quantificacao,
    analisar_verbos_de_acao,
    calcular_pontuacoes,
    analisar_palavras_chave,
    gerar_feedback_qualitativo_gemini,
    analisar_curriculo_completo,
    analisar_curriculo_com_agno,
    verificar_saude_agno
)
from app.schemas.curriculum import (
    CurriculumCreate,
    CurriculumUpdate,
    CurriculumResponse,
    CurriculumAnalysisResponse,
    CurriculumAnalysis
)
from app.utils.file_utils import (
    extrair_texto_de_pdf, 
    validar_arquivo_pdf, 
    salvar_arquivo_pdf
)
from app.models.user import User
from app.models.curriculum import Curriculum
from app.models.metrics import Metrics
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/curriculum", tags=["curriculum"])


def get_curriculum_service(db: AsyncSession = Depends(get_db)) -> ICurriculumService:
    """Dependency injection para o serviço de currículos."""
    repository = CurriculumRepository(db)
    from app.agno.analysis_engine import AnalysisEngine
    analysis_engine = AnalysisEngine()
    return CurriculumService(repository, analysis_engine)


@router.post("/upload", response_model=CurriculumAnalysis)
async def upload_curriculum(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    file: UploadFile = File(...),
    job_description: str = Form(None)
):
    """
    Endpoint para upload e análise de um currículo em PDF.
    
    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        file: Arquivo PDF do currículo
        job_description: Descrição da vaga (opcional)
        
    Returns:
        CurriculumAnalysis: Resultado completo da análise
    """
    try:
        # Valida o arquivo PDF
        validar_arquivo_pdf(file)
        
        # Extrai o texto do PDF
        texto_cv = await extrair_texto_de_pdf(file)
        if not texto_cv:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Não foi possível extrair texto do PDF."
            )
        
        # Salva o arquivo físico
        from app.core.config import settings
        unique_filename = f"{current_user.id}_{uuid.uuid4()}_{file.filename}"
        file_path = await salvar_arquivo_pdf(file, settings.upload_dir, unique_filename)
        
        # Executa análise completa usando o orquestrador Agno
        resultado_final = analisar_curriculo_com_agno(texto_cv, job_description)
        
        # Se houver erro no Agno, usa análise tradicional como fallback
        if "error" in resultado_final:
            logger.warning(f"Erro no Agno: {resultado_final['error']}, usando análise tradicional")
            
            # Executa as análises estruturais com spaCy
            analise_quant = analisar_quantificacao(texto_cv)
            analise_verbos = analisar_verbos_de_acao(texto_cv)
            pontuacoes = calcular_pontuacoes(analise_quant, analise_verbos)
            
            # Executa a análise qualitativa com Gemini
            feedback_gemini = gerar_feedback_qualitativo_gemini(texto_cv)
            
            # Compila o resultado final
            resultado_final = {
                "feedback_qualitativo": feedback_gemini,
                "quantificacao": analise_quant,
                "verbos_de_acao": analise_verbos,
                "pontuacoes": pontuacoes,
            }
            
            if job_description:
                resultado_final["palavras_chave"] = analisar_palavras_chave(texto_cv, job_description)
        
        # Persiste os dados no banco
        db_curriculum = Curriculum(
            user_id=current_user.id,
            filename=file.filename,
            file_path=file_path,
            analysis_result=json.dumps(resultado_final, ensure_ascii=False)
        )
        db.add(db_curriculum)
        db.flush()  # Usa flush para obter o ID do currículo antes do commit
        
        # Extrai pontuações do resultado do Agno ou da análise tradicional
        if "pontuacoes" in resultado_final:
            pontuacoes = resultado_final["pontuacoes"]
            action_verbs_score = pontuacoes.get("pontuacao_verbos_acao", 0.0)
            quantification_score = pontuacoes.get("pontuacao_quantificacao", 0.0)
            overall_score = pontuacoes.get("pontuacao_geral", 0.0)
        else:
            # Fallback para análise tradicional
            action_verbs_score = 0.0
            quantification_score = 0.0
            overall_score = 0.0
        
        db_metrics = Metrics(
            curriculum_id=db_curriculum.id,
            action_verbs_score=action_verbs_score,
            quantification_score=quantification_score,
            overall_score=overall_score
        )
        db.add(db_metrics)
        db.commit()
        db.refresh(db_curriculum)
        
        return {
            "curriculum_info": db_curriculum,
            "analysis": resultado_final
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no upload do currículo: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=CurriculumResponse)
async def create_curriculum(
    curriculum: CurriculumCreate,
    service: ICurriculumService = Depends(get_curriculum_service)
):
    """Cria um novo currículo."""
    try:
        return await service.create_curriculum(curriculum)
    except Exception as e:
        logger.error(f"Erro ao criar currículo: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{curriculum_id}", response_model=CurriculumResponse)
async def get_curriculum(
    curriculum_id: int,
    service: ICurriculumService = Depends(get_curriculum_service)
):
    """Busca um currículo por ID."""
    try:
        return await service.get_curriculum(curriculum_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao buscar currículo: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/", response_model=List[CurriculumResponse])
async def list_curriculums(
    skip: int = 0,
    limit: int = 100,
    service: ICurriculumService = Depends(get_curriculum_service)
):
    """Lista todos os currículos."""
    try:
        return await service.list_curriculums(skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Erro ao listar currículos: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/list")
async def list_curricula(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista todos os currículos do usuário autenticado.
    
    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        Lista de currículos do usuário
    """
    try:
        result = db.execute(
            select(Curriculum).where(Curriculum.user_id == current_user.id)
        )
        curricula = result.scalars().all()
        
        return [
            {
                "id": curriculum.id,
                "filename": curriculum.filename,
                "upload_date": curriculum.upload_date,
                "file_path": curriculum.file_path
            }
            for curriculum in curricula
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar currículos: {str(e)}"
        )


@router.put("/{curriculum_id}", response_model=CurriculumResponse)
async def update_curriculum(
    curriculum_id: int,
    curriculum: CurriculumUpdate,
    service: ICurriculumService = Depends(get_curriculum_service)
):
    """Atualiza um currículo."""
    try:
        return await service.update_curriculum(curriculum_id, curriculum)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao atualizar currículo: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.delete("/{curriculum_id}")
async def delete_curriculum(
    curriculum_id: int,
    service: ICurriculumService = Depends(get_curriculum_service)
):
    """Remove um currículo."""
    try:
        success = await service.delete_curriculum(curriculum_id)
        if not success:
            raise HTTPException(status_code=404, detail="Currículo não encontrado")
        return {"message": "Currículo removido com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao remover currículo: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")





@router.post("/{curriculum_id}/analyze", response_model=CurriculumAnalysisResponse)
async def analyze_curriculum(
    curriculum_id: int,
    service: ICurriculumService = Depends(get_curriculum_service)
):
    """Analisa um currículo específico."""
    try:
        analysis_result = await service.analyze_curriculum_content(curriculum_id)
        return CurriculumAnalysisResponse(
            curriculum_id=curriculum_id,
            analysis=analysis_result
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Erro na análise do currículo: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.post("/analyze-text")
async def analyze_text(
    text: str,
    service: ICurriculumService = Depends(get_curriculum_service)
):
    """Analisa texto diretamente sem salvar no banco."""
    try:
        from app.agno.analysis_engine import AnalysisEngine
        analysis_engine = AnalysisEngine()
        result = await analysis_engine.analyze_curriculum(text)
        return result
    except Exception as e:
        logger.error(f"Erro na análise de texto: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/test-agno")
async def test_agno():
    """
    Endpoint de teste para verificar o funcionamento do Agno.
    
    Returns:
        Status das ferramentas de análise
    """
    try:
        health_status = verificar_saude_agno()
        return {
            "status": "success",
            "agno_health": health_status,
            "message": "Agno está funcionando corretamente"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Erro ao verificar status do Agno"
        }
