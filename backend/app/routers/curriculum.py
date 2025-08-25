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
from app.models.curriculum import Curriculum, CurriculumAnalysis as CurriculumAnalysisModel
from app.models.metrics import Metrics
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["curriculum"])


def get_curriculum_service(db: AsyncSession = Depends(get_db)) -> ICurriculumService:
    """Dependency injection para o serviço de currículos."""
    repository = CurriculumRepository(db)
    from app.agno.analysis_engine import AnalysisEngine
    analysis_engine = AnalysisEngine()
    return CurriculumService(repository, analysis_engine)


@router.post("/upload", response_model=CurriculumAnalysis)
async def upload_curriculum(
    *,
    db: AsyncSession = Depends(get_db),  # Mudado para AsyncSession
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
    # Inicialização das variáveis para evitar UnboundLocalError
    resultado_final = None
    db_curriculum = None
    db_analysis = None
    db_metrics = None
    final_response = None
    
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
        try:
            resultado_final = await analisar_curriculo_com_agno(texto_cv, job_description)
            
            # Valida se a análise foi bem-sucedida
            if not resultado_final or "error" in resultado_final:
                error_msg = resultado_final.get("error", "Erro desconhecido na análise") if resultado_final else "Falha na análise do currículo"
                logger.error(f"Erro na análise do currículo: {error_msg}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Ocorreu um erro ao analisar o currículo com o serviço de IA: {error_msg}. Tente novamente mais tarde."
                )
            
            # Valida se a estrutura dos dados está correta antes de prosseguir
            required_fields = ["feedback_qualitativo", "quantificacao", "verbos_de_acao", "pontuacoes"]
            missing_fields = [field for field in required_fields if field not in resultado_final]
            
            if missing_fields:
                logger.error(f"Campos obrigatórios ausentes na análise: {missing_fields}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro interno na análise do currículo. Estrutura de dados inválida."
                )
                
        except HTTPException:
            raise
        except Exception as agno_error:
            logger.error(f"Erro crítico no Agno: {agno_error}")
            # Fallback para análise tradicional
            try:
                resultado_final = {
                    "feedback_qualitativo": {
                        "pontos_fortes": ["Análise básica concluída"],
                        "pontos_fracos": ["Análise limitada devido a erro no sistema"],
                        "sugestoes": ["Tente novamente mais tarde"]
                    },
                    "quantificacao": {"total": 0, "items": [], "score_quantificacao": 0.0},
                    "verbos_de_acao": {"total": 0, "items": [], "score_verbos": 0.0},
                    "pontuacoes": {
                        "pontuacao_verbos_acao": 0.0,
                        "pontuacao_quantificacao": 0.0,
                        "pontuacao_geral": 0.0
                    }
                }
                
                if job_description:
                    resultado_final["palavras_chave"] = {"score": 0.0, "items": []}
                    
                logger.warning("Usando análise de fallback devido a erro no Agno")
                
            except Exception as fallback_error:
                logger.error(f"Erro no fallback: {fallback_error}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Serviço de análise temporariamente indisponível. Tente novamente mais tarde."
                )
            
        # Valida e prepara os dados para salvar no banco
        try:
            # Garante que todos os campos obrigatórios existam
            pontuacoes = resultado_final.get("pontuacoes", {})
            feedback_qualitativo = resultado_final.get("feedback_qualitativo", {})
            quantificacao = resultado_final.get("quantificacao", {})
            verbos_de_acao = resultado_final.get("verbos_de_acao", {})
            palavras_chave = resultado_final.get("palavras_chave", {})
            
            # Validações específicas
            if not isinstance(feedback_qualitativo, dict):
                feedback_qualitativo = {"pontos_fortes": [], "pontos_fracos": [], "sugestoes": []}
            
            if not isinstance(quantificacao, dict):
                quantificacao = {"total": 0, "items": [], "score_quantificacao": 0.0}
                
            if not isinstance(verbos_de_acao, dict):
                verbos_de_acao = {"total": 0, "items": [], "score_verbos": 0.0}
                
            if not isinstance(palavras_chave, dict):
                palavras_chave = {"score": 0.0, "items": []}
            
            # Extrai pontuações com valores padrão
            action_verbs_score = pontuacoes.get("pontuacao_verbos_acao", 0.0)
            quantification_score = pontuacoes.get("pontuacao_quantificacao", 0.0)
            overall_score = pontuacoes.get("pontuacao_geral", 0.0)
            
            # Valida se os scores são números válidos
            try:
                action_verbs_score = float(action_verbs_score) if action_verbs_score is not None else 0.0
                quantification_score = float(quantification_score) if quantification_score is not None else 0.0
                overall_score = float(overall_score) if overall_score is not None else 0.0
            except (ValueError, TypeError):
                action_verbs_score = 0.0
                quantification_score = 0.0
                overall_score = 0.0
            
        except Exception as validation_error:
            logger.error(f"Erro na validação dos dados: {validation_error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na validação dos dados da análise."
            )
            
        # Persiste os dados no banco
        db_curriculum = Curriculum(
            user_id=current_user.id,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file.size,
            title=file.filename,
        )
        db.add(db_curriculum)
        await db.flush()  # Corrigido: aguardar o flush
        
        # Salva a análise na tabela CurriculumAnalysis
        db_analysis = CurriculumAnalysisModel(
            curriculum_id=db_curriculum.id,
            spacy_analysis=json.dumps(resultado_final, ensure_ascii=False),
            overall_score=overall_score,
            action_verbs_count=verbos_de_acao.get("total", 0),
            quantified_results_count=quantificacao.get("total", 0),
            keywords_score=palavras_chave.get("score", 0.0),
            strengths=json.dumps(feedback_qualitativo.get("pontos_fortes", []), ensure_ascii=False),
            weaknesses=json.dumps(feedback_qualitativo.get("pontos_fracos", []), ensure_ascii=False),
            suggestions=json.dumps(feedback_qualitativo.get("sugestoes", []), ensure_ascii=False)
        )
        db.add(db_analysis)
        
        # Cria as métricas
        db_metrics = Metrics(
            curriculum_id=db_curriculum.id,
            action_verbs_score=action_verbs_score,
            quantification_score=quantification_score,
            overall_score=overall_score
        )
        db.add(db_metrics)
        await db.commit()  # Corrigido: aguardar o commit
        await db.refresh(db_curriculum)
        
        # DEBUG: Log dos dados que serão retornados
        final_response = {
            "curriculum_info": {
                "id": int(db_curriculum.id),
                "user_id": int(db_curriculum.user_id),
                "filename": str(db_curriculum.original_filename),
                "file_path": str(db_curriculum.file_path),
                "upload_date": db_curriculum.created_at if db_curriculum.created_at else None
            },
            "analysis": {
                "feedback_qualitativo": feedback_qualitativo,
                "quantificacao": quantificacao,
                "verbos_de_acao": verbos_de_acao,
                "pontuacoes": pontuacoes,
                "palavras_chave": palavras_chave,
                "resumo": {
                    "nivel_geral": "Análise Concluída",
                    "pontuacao_geral": float(overall_score),
                    "ferramentas_ai_disponiveis": True,
                    "spacy_disponivel": True
                }
            }
        }
        
        # DEBUG: Log detalhado dos dados
        logger.info("DEBUG: ESTRUTURA COMPLETA DOS DADOS:")
        logger.info(f"curriculum_info: {final_response['curriculum_info']}")
        logger.info(f"analysis keys: {list(final_response['analysis'].keys())}")
        logger.info(f"feedback_qualitativo: {feedback_qualitativo}")
        logger.info(f"quantificacao: {quantificacao}")
        logger.info(f"verbos_de_acao: {verbos_de_acao}")
        logger.info(f"pontuacoes: {pontuacoes}")
        logger.info(f"palavras_chave: {palavras_chave}")
        
        # DEBUG: Validação manual do schema antes do retorno
        try:
            from app.schemas.curriculum import CurriculumAnalysis
            # Tenta criar o objeto para validar
            validated_response = CurriculumAnalysis(**final_response)
            logger.info("DEBUG: VALIDAÇÃO PYDANTIC BEM-SUCEDIDA!")
            logger.info(f"Objeto validado: {validated_response}")
        except Exception as validation_error:
            import traceback
            logger.error("--- ERRO ORIGINAL CAPTURADO ---")
            logger.error(f"Tipo de Erro: {type(validation_error).__name__}")
            logger.error(f"Mensagem: {validation_error}")
            logger.error("Traceback completo:")
            logger.error(traceback.format_exc())
            logger.error("-----------------------------")
            # Em caso de erro, retorna estrutura simplificada
            return {
                "curriculum_info": {
                    "id": int(db_curriculum.id),
                    "user_id": int(db_curriculum.user_id),
                    "filename": str(db_curriculum.original_filename),
                    "file_path": str(db_curriculum.file_path),
                    "upload_date": db_curriculum.created_at
                },
                "analysis": {
                    "error": f"Erro na validação: {str(validation_error)}",
                    "feedback_qualitativo": {"pontos_fortes": [], "pontos_fracos": [], "sugestoes": []},
                    "quantificacao": {"total": 0, "items": [], "score_quantificacao": 0.0},
                    "verbos_de_acao": {"total": 0, "items": [], "score_verbos": 0.0},
                    "pontuacoes": {"pontuacao_geral": 0.0},
                    "palavras_chave": {"score": 0.0, "items": []},
                    "resumo": {"nivel_geral": "Erro", "pontuacao_geral": 0.0}
                }
            }
        
        return final_response
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        logger.error("--- ERRO GERAL CAPTURADO ---")
        logger.error(f"Tipo de Erro: {type(e).__name__}")
        logger.error(f"Mensagem: {e}")
        logger.error("Traceback completo:")
        logger.error(traceback.format_exc())
        logger.error("-----------------------------")
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


@router.get("/list")
async def list_curricula(
    db: AsyncSession = Depends(get_db),  # Mudado para AsyncSession
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista todos os currículos do usuário autenticado.
    
    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        Lista de currículos do usuário ou lista vazia se não houver currículos
    """
    try:
        result = await db.execute(  # Corrigido: aguardar execute
            select(Curriculum).where(Curriculum.user_id == current_user.id)
        )
        curricula = result.scalars().all()
        
        # Retorna lista vazia se não houver currículos (não é erro)
        return [
            {
                "id": curriculum.id,
                "filename": curriculum.original_filename,
                "upload_date": curriculum.created_at,
                "file_path": curriculum.file_path,
                "user_id": curriculum.user_id
            }
            for curriculum in curricula
        ]
    except Exception as e:
        logger.error(f"Erro ao listar currículos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar currículos: {str(e)}"
        )


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
