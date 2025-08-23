from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional
from datetime import datetime, timedelta
import json

from app.models.user import User
from app.models.curriculum import Curriculum, CurriculumVersion, CurriculumAnalysis
from app.schemas.metrics import (
    TimeSeriesMetricsResponse,
    CurriculumVersionMetrics,
    CurriculumMetrics,
)
from app.core.database import get_db
from app.api.dependencies import get_current_user

router = APIRouter()


@router.get("/time-series", response_model=TimeSeriesMetricsResponse)
async def get_curriculum_time_series_metrics(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    Retorna uma série temporal de dados com as métricas e pontuações de cada versão
    de currículo enviado por um usuário, para visualização em gráfico no frontend.

    Args:
        current_user: Usuário autenticado
        db: Sessão do banco de dados

    Returns:
        TimeSeriesMetricsResponse: Série temporal de métricas dos currículos do usuário
    """
    try:
        # 1. Identificar o usuário e recuperar todas as versões de currículo associadas a ele
        # Busca todas as análises de currículos do usuário, ordenadas por data
        result = await db.execute(
            select(CurriculumAnalysis)
            .join(Curriculum, CurriculumAnalysis.curriculum_id == Curriculum.id)
            .where(Curriculum.user_id == current_user.id)
            .order_by(CurriculumAnalysis.analysis_date)
        )
        analyses = result.scalars().all()

        if not analyses:
            # Retorna resposta vazia se não há análises
            return TimeSeriesMetricsResponse(
                user_id=current_user.id,
                total_versions=0,
                time_series=[],
                average_score=0.0,
                best_score=0.0,
                improvement_rate=0.0,
            )

        # 2. Para cada versão de currículo, extrair métricas
        time_series_data = []
        scores = []

        for i, analysis in enumerate(analyses):
            # Determinar o ID da versão
            if analysis.version_id:
                # Se tem versão específica, buscar informações da versão
                version_result = await db.execute(
                    select(CurriculumVersion).where(
                        CurriculumVersion.id == analysis.version_id
                    )
                )
                version = version_result.scalar_one_or_none()
                version_id = (
                    f"v{version.version_number}"
                    if version
                    else f"analysis_{analysis.id}"
                )
            else:
                # Se não tem versão específica, usar o currículo principal
                version_id = f"curriculum_{analysis.curriculum_id}"

            # Extrair métricas da análise
            metrics = _extract_metrics_from_analysis(analysis)

            # Criar entrada da série temporal
            time_series_entry = CurriculumVersionMetrics(
                version_id=version_id, timestamp=analysis.analysis_date, metrics=metrics
            )

            time_series_data.append(time_series_entry)
            scores.append(metrics.score)

        # 3. Calcular estatísticas
        total_versions = len(time_series_data)
        average_score = sum(scores) / total_versions if scores else 0.0
        best_score = max(scores) if scores else 0.0

        # Calcular taxa de melhoria (comparar primeira com última análise)
        improvement_rate = 0.0
        if len(scores) >= 2:
            first_score = scores[0]
            last_score = scores[-1]
            if first_score > 0:
                improvement_rate = ((last_score - first_score) / first_score) * 100

        return TimeSeriesMetricsResponse(
            user_id=current_user.id,
            total_versions=total_versions,
            time_series=time_series_data,
            average_score=round(average_score, 2),
            best_score=round(best_score, 2),
            improvement_rate=round(improvement_rate, 2),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar série temporal de métricas: {str(e)}",
        )


@router.get("/time-series/filtered", response_model=TimeSeriesMetricsResponse)
async def get_filtered_time_series_metrics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    min_score: Optional[float] = None,
    max_score: Optional[float] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retorna uma série temporal filtrada de métricas de currículos.

    Args:
        start_date: Data de início para filtrar (opcional)
        end_date: Data de fim para filtrar (opcional)
        min_score: Score mínimo para filtrar (opcional)
        max_score: Score máximo para filtrar (opcional)
        current_user: Usuário autenticado
        db: Sessão do banco de dados

    Returns:
        TimeSeriesMetricsResponse: Série temporal filtrada de métricas
    """
    try:
        # Construir query base
        query = (
            select(CurriculumAnalysis)
            .join(Curriculum, CurriculumAnalysis.curriculum_id == Curriculum.id)
            .where(Curriculum.user_id == current_user.id)
        )

        # Aplicar filtros de data
        if start_date:
            query = query.where(CurriculumAnalysis.analysis_date >= start_date)
        if end_date:
            query = query.where(CurriculumAnalysis.analysis_date <= end_date)

        # Aplicar filtros de score
        if min_score is not None:
            query = query.where(CurriculumAnalysis.overall_score >= min_score)
        if max_score is not None:
            query = query.where(CurriculumAnalysis.overall_score <= max_score)

        # Ordenar por data
        query = query.order_by(CurriculumAnalysis.analysis_date)

        # Executar query
        result = await db.execute(query)
        analyses = result.scalars().all()

        if not analyses:
            return TimeSeriesMetricsResponse(
                user_id=current_user.id,
                total_versions=0,
                time_series=[],
                average_score=0.0,
                best_score=0.0,
                improvement_rate=0.0,
            )

        # Processar análises (mesmo código do endpoint principal)
        time_series_data = []
        scores = []

        for analysis in analyses:
            # Determinar o ID da versão
            if analysis.version_id:
                version_result = await db.execute(
                    select(CurriculumVersion).where(
                        CurriculumVersion.id == analysis.version_id
                    )
                )
                version = version_result.scalar_one_or_none()
                version_id = (
                    f"v{version.version_number}"
                    if version
                    else f"analysis_{analysis.id}"
                )
            else:
                version_id = f"curriculum_{analysis.curriculum_id}"

            # Extrair métricas da análise
            metrics = _extract_metrics_from_analysis(analysis)

            # Criar entrada da série temporal
            time_series_entry = CurriculumVersionMetrics(
                version_id=version_id, timestamp=analysis.analysis_date, metrics=metrics
            )

            time_series_data.append(time_series_entry)
            scores.append(metrics.score)

        # Calcular estatísticas
        total_versions = len(time_series_data)
        average_score = sum(scores) / total_versions if scores else 0.0
        best_score = max(scores) if scores else 0.0

        # Calcular taxa de melhoria
        improvement_rate = 0.0
        if len(scores) >= 2:
            first_score = scores[0]
            last_score = scores[-1]
            if first_score > 0:
                improvement_rate = ((last_score - first_score) / first_score) * 100

        return TimeSeriesMetricsResponse(
            user_id=current_user.id,
            total_versions=total_versions,
            time_series=time_series_data,
            average_score=round(average_score, 2),
            best_score=round(best_score, 2),
            improvement_rate=round(improvement_rate, 2),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar série temporal filtrada: {str(e)}",
        )


def _extract_metrics_from_analysis(analysis: CurriculumAnalysis) -> CurriculumMetrics:
    """
    Extrai métricas padronizadas de uma análise de currículo.

    Args:
        analysis: Análise de currículo do banco de dados

    Returns:
        CurriculumMetrics: Métricas padronizadas
    """
    # Pontuação geral (já existe no modelo)
    overall_score = analysis.overall_score or 0.0

    # Extrair métricas das análises JSON
    spacy_data = analysis.spacy_analysis or {}
    gemini_data = analysis.gemini_analysis or {}

    # Calcular clareza textual baseada em estatísticas do spaCy
    clarity = _calculate_clarity_score(spacy_data, analysis)

    # Calcular relevância baseada na análise do Gemini
    relevance = _calculate_relevance_score(gemini_data)

    # Calcular score de palavras-chave
    keywords_score = analysis.keywords_score or 0.0

    # Calcular estrutura baseada em métricas quantitativas
    structure = _calculate_structure_score(analysis)

    # Calcular personalização baseada na análise do Gemini
    personalization = _calculate_personalization_score(gemini_data)

    return CurriculumMetrics(
        score=overall_score,
        clarity=clarity,
        relevance=relevance,
        keywords=keywords_score,
        structure=structure,
        personalization=personalization,
    )


def _calculate_clarity_score(spacy_data: dict, analysis: CurriculumAnalysis) -> float:
    """Calcula score de clareza textual baseado na análise do spaCy."""
    try:
        # Baseado em estatísticas de texto e verbos de ação
        action_verbs = analysis.action_verbs_count or 0
        quantified_results = analysis.quantified_results_count or 0

        # Score baseado na presença de verbos de ação e resultados quantificados
        clarity_score = min(100.0, (action_verbs * 5) + (quantified_results * 10))

        # Normalizar para 0-100
        return min(100.0, max(0.0, clarity_score))
    except:
        return 50.0  # Score padrão


def _calculate_relevance_score(gemini_data: dict) -> float:
    """Calcula score de relevância baseado na análise do Gemini."""
    try:
        # Verificar se há avaliação de relevância da indústria
        industry_relevance = gemini_data.get("industry_relevance", "")

        # Mapear avaliações textuais para scores
        relevance_mapping = {
            "high": 85.0,
            "medium": 60.0,
            "low": 30.0,
            "excellent": 95.0,
            "good": 75.0,
            "fair": 50.0,
            "poor": 25.0,
        }

        # Buscar por palavras-chave na avaliação
        for keyword, score in relevance_mapping.items():
            if keyword.lower() in industry_relevance.lower():
                return score

        return 60.0  # Score padrão
    except:
        return 60.0


def _calculate_structure_score(analysis: CurriculumAnalysis) -> float:
    """Calcula score de estrutura baseado em métricas quantitativas."""
    try:
        # Baseado em diferentes aspectos estruturais
        base_score = 50.0

        # Adicionar pontos por verbos de ação
        if analysis.action_verbs_count:
            base_score += min(20.0, analysis.action_verbs_count * 2)

        # Adicionar pontos por resultados quantificados
        if analysis.quantified_results_count:
            base_score += min(20.0, analysis.quantified_results_count * 3)

        # Adicionar pontos por score de palavras-chave
        if analysis.keywords_score:
            base_score += min(10.0, analysis.keywords_score * 0.1)

        return min(100.0, max(0.0, base_score))
    except:
        return 50.0


def _calculate_personalization_score(gemini_data: dict) -> float:
    """Calcula score de personalização baseado na análise do Gemini."""
    try:
        # Verificar sugestões de personalização
        suggestions = gemini_data.get("suggestions", [])
        strengths = gemini_data.get("strengths", [])

        # Score baseado na quantidade e qualidade de sugestões
        personalization_score = 50.0

        # Adicionar pontos por sugestões específicas
        if suggestions:
            personalization_score += min(30.0, len(suggestions) * 3)

        # Adicionar pontos por pontos fortes identificados
        if strengths:
            personalization_score += min(20.0, len(strengths) * 2)

        return min(100.0, max(0.0, personalization_score))
    except:
        return 50.0
