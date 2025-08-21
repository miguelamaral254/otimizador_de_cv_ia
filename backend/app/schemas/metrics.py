from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class ProgressMetrics(BaseModel):
    """Schema para métricas de progresso do usuário."""
    total_curriculum: int
    total_analyses: int
    average_score: float
    best_score: float
    improvement_rate: float  
    last_analysis_date: Optional[datetime] = None


class ScoreTrend(BaseModel):
    """Schema para tendência de pontuação ao longo do tempo."""
    date: datetime
    score: float
    curriculum_id: int
    version_number: Optional[int] = None


class ScoreTrendResponse(BaseModel):
    """Schema para resposta de tendência de pontuação."""
    trends: List[ScoreTrend]
    period: str  # "week", "month", "year"
    average_improvement: float


class KeywordAnalysis(BaseModel):
    """Schema para análise de palavras-chave."""
    keyword: str
    frequency: int
    relevance_score: float
    industry_match: bool


class IndustryInsights(BaseModel):
    """Schema para insights específicos da indústria."""
    industry: str
    recommended_keywords: List[str]
    trending_skills: List[str]
    market_demand: str  # "high", "medium", "low"


class ComparativeAnalysis(BaseModel):
    """Schema para análise comparativa entre versões."""
    current_version: int
    previous_version: int
    score_difference: float
    improvements: List[str]
    regressions: List[str]
    overall_progress: str  # "improving", "stable", "declining"


class DashboardResponse(BaseModel):
    """Schema para resposta do dashboard principal."""
    user_metrics: ProgressMetrics
    recent_analyses: List[Dict[str, Any]]
    score_trends: ScoreTrendResponse
    top_keywords: List[KeywordAnalysis]
    industry_insights: Optional[IndustryInsights] = None
    recommendations: List[str]


class ReportFilters(BaseModel):
    """Schema para filtros de relatórios."""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None
    industry: Optional[str] = None
    include_versions: bool = True


class ReportResponse(BaseModel):
    """Schema para resposta de relatório."""
    generated_at: datetime
    filters: ReportFilters
    summary: Dict[str, Any]
    detailed_data: List[Dict[str, Any]]
    charts_data: Dict[str, Any]  # Dados para gráficos
    recommendations: List[str]
