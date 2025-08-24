"""
Router para operações relacionadas a currículos.

Este módulo contém os endpoints para upload, análise e gerenciamento de currículos.
"""

import json
import os
import uuid
import logging
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

logger = logging.getLogger(__name__)

from app.models.user import User
from app.models.curriculum import Curriculum
from app.models.metrics import Metrics
from app.schemas.curriculum import CurriculumAnalysis
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.analysis import (
    analisar_quantificacao,
    analisar_verbos_de_acao,
    calcular_pontuacoes,
    analisar_palavras_chave,
    gerar_feedback_qualitativo_gemini,
    analisar_curriculo_completo,
    analisar_curriculo_com_agno
)
from app.utils.file_utils import extrair_texto_de_pdf, validar_arquivo_pdf, salvar_arquivo_pdf

router = APIRouter()

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

@router.get("/test-agno")
async def test_agno():
    """
    Endpoint de teste para verificar o funcionamento do Agno.
    
    Returns:
        Status das ferramentas de análise
    """
    try:
        from app.analysis import verificar_saude_agno
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

@router.get("/{curriculum_id}")
async def get_curriculum(
    curriculum_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtém detalhes de um currículo específico.
    
    Args:
        curriculum_id: ID do currículo
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        Detalhes do currículo
    """
    try:
        result = db.execute(
            select(Curriculum).where(
                Curriculum.id == curriculum_id,
                Curriculum.user_id == current_user.id
            )
        )
        curriculum = result.scalar_one_or_none()
        
        if not curriculum:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Currículo não encontrado"
            )
        
        return {
            "id": curriculum.id,
            "filename": curriculum.filename,
            "upload_date": curriculum.upload_date,
            "file_path": curriculum.file_path,
            "analysis_result": json.loads(curriculum.analysis_result) if curriculum.analysis_result else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.delete("/{curriculum_id}")
async def delete_curriculum(
    curriculum_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove um currículo específico.
    
    Args:
        curriculum_id: ID do currículo
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        Confirmação de remoção
    """
    try:
        result = db.execute(
            select(Curriculum).where(
                Curriculum.id == curriculum_id,
                Curriculum.user_id == current_user.id
            )
        )
        curriculum = result.scalar_one_or_none()
        
        if not curriculum:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Currículo não encontrado"
            )
        
        # Remove o arquivo físico
        if os.path.exists(curriculum.file_path):
            os.remove(curriculum.file_path)
        
        # Remove do banco de dados
        db.delete(curriculum)
        db.commit()
        
        return {"message": "Currículo removido com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )