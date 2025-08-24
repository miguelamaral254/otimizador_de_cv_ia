"""
Testes unitários para app/schemas/metrics.py
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.metrics import (
    ProgressMetrics,
    ScoreTrend,
    ScoreTrendResponse,
    KeywordAnalysis,
    IndustryInsights,
    ComparativeAnalysis,
    DashboardResponse,
    ReportFilters,
    ReportResponse,
    CurriculumMetrics,
    CurriculumVersionMetrics,
    TimeSeriesMetricsResponse
)


class TestProgressMetrics:
    """Testa o schema ProgressMetrics."""
    
    def test_progress_metrics_valid(self):
        """Testa criação válida de ProgressMetrics."""
        now = datetime.now()
        data = {
            "total_curriculum": 5,
            "total_analyses": 10,
            "average_score": 7.5,
            "best_score": 9.2,
            "improvement_rate": 15.5,
            "last_analysis_date": now
        }
        metrics = ProgressMetrics(**data)
        assert metrics.total_curriculum == 5
        assert metrics.total_analyses == 10
        assert metrics.average_score == 7.5
        assert metrics.best_score == 9.2
        assert metrics.improvement_rate == 15.5
        assert metrics.last_analysis_date == now
    
    def test_progress_metrics_optional_last_analysis_date(self):
        """Testa last_analysis_date opcional."""
        data = {
            "total_curriculum": 3,
            "total_analyses": 6,
            "average_score": 8.0,
            "best_score": 9.0,
            "improvement_rate": 12.0
        }
        metrics = ProgressMetrics(**data)
        assert metrics.last_analysis_date is None


class TestScoreTrend:
    """Testa o schema ScoreTrend."""
    
    def test_score_trend_valid(self):
        """Testa criação válida de ScoreTrend."""
        now = datetime.now()
        data = {
            "date": now,
            "score": 8.5,
            "curriculum_id": 123,
            "version_number": 2
        }
        trend = ScoreTrend(**data)
        assert trend.date == now
        assert trend.score == 8.5
        assert trend.curriculum_id == 123
        assert trend.version_number == 2
    
    def test_score_trend_optional_version_number(self):
        """Testa version_number opcional."""
        now = datetime.now()
        data = {
            "date": now,
            "score": 7.8,
            "curriculum_id": 456
        }
        trend = ScoreTrend(**data)
        assert trend.version_number is None


class TestScoreTrendResponse:
    """Testa o schema ScoreTrendResponse."""
    
    def test_score_trend_response_valid(self):
        """Testa criação válida de ScoreTrendResponse."""
        now = datetime.now()
        trend_data = {
            "date": now,
            "score": 8.0,
            "curriculum_id": 123
        }
        
        data = {
            "trends": [ScoreTrend(**trend_data)],
            "period": "month",
            "average_improvement": 5.2
        }
        
        response = ScoreTrendResponse(**data)
        assert len(response.trends) == 1
        assert response.period == "month"
        assert response.average_improvement == 5.2


class TestKeywordAnalysis:
    """Testa o schema KeywordAnalysis."""
    
    def test_keyword_analysis_valid(self):
        """Testa criação válida de KeywordAnalysis."""
        data = {
            "keyword": "Python",
            "frequency": 15,
            "relevance_score": 9.2,
            "industry_match": True
        }
        analysis = KeywordAnalysis(**data)
        assert analysis.keyword == "Python"
        assert analysis.frequency == 15
        assert analysis.relevance_score == 9.2
        assert analysis.industry_match is True


class TestIndustryInsights:
    """Testa o schema IndustryInsights."""
    
    def test_industry_insights_valid(self):
        """Testa criação válida de IndustryInsights."""
        data = {
            "industry": "Technology",
            "recommended_keywords": ["Python", "Django", "React"],
            "trending_skills": ["Machine Learning", "Cloud Computing"],
            "market_demand": "high"
        }
        insights = IndustryInsights(**data)
        assert insights.industry == "Technology"
        assert len(insights.recommended_keywords) == 3
        assert len(insights.trending_skills) == 2
        assert insights.market_demand == "high"


class TestComparativeAnalysis:
    """Testa o schema ComparativeAnalysis."""
    
    def test_comparative_analysis_valid(self):
        """Testa criação válida de ComparativeAnalysis."""
        data = {
            "current_version": 3,
            "previous_version": 2,
            "score_difference": 1.5,
            "improvements": ["Melhor formatação", "Mais palavras-chave"],
            "regressions": ["Texto muito longo"],
            "overall_progress": "improving"
        }
        analysis = ComparativeAnalysis(**data)
        assert analysis.current_version == 3
        assert analysis.previous_version == 2
        assert analysis.score_difference == 1.5
        assert len(analysis.improvements) == 2
        assert len(analysis.regressions) == 1
        assert analysis.overall_progress == "improving"


class TestDashboardResponse:
    """Testa o schema DashboardResponse."""
    
    def test_dashboard_response_valid(self):
        """Testa criação válida de DashboardResponse."""
        now = datetime.now()
        
        progress_data = {
            "total_curriculum": 5,
            "total_analyses": 10,
            "average_score": 7.5,
            "best_score": 9.2,
            "improvement_rate": 15.5
        }
        
        trend_data = {
            "date": now,
            "score": 8.0,
            "curriculum_id": 123
        }
        
        score_trends_data = {
            "trends": [ScoreTrend(**trend_data)],
            "period": "month",
            "average_improvement": 5.2
        }
        
        keyword_data = {
            "keyword": "Python",
            "frequency": 15,
            "relevance_score": 9.2,
            "industry_match": True
        }
        
        industry_data = {
            "industry": "Technology",
            "recommended_keywords": ["Python", "Django"],
            "trending_skills": ["Machine Learning"],
            "market_demand": "high"
        }
        
        data = {
            "user_metrics": ProgressMetrics(**progress_data),
            "recent_analyses": [{"id": 1, "score": 8.5}],
            "score_trends": ScoreTrendResponse(**score_trends_data),
            "top_keywords": [KeywordAnalysis(**keyword_data)],
            "industry_insights": IndustryInsights(**industry_data),
            "recommendations": ["Melhorar formatação", "Adicionar projetos"]
        }
        
        response = DashboardResponse(**data)
        assert response.user_metrics.total_curriculum == 5
        assert len(response.recent_analyses) == 1
        assert response.score_trends.period == "month"
        assert len(response.top_keywords) == 1
        assert response.industry_insights.industry == "Technology"
        assert len(response.recommendations) == 2
    
    def test_dashboard_response_optional_industry_insights(self):
        """Testa industry_insights opcional."""
        now = datetime.now()
        
        progress_data = {
            "total_curriculum": 3,
            "total_analyses": 6,
            "average_score": 8.0,
            "best_score": 9.0,
            "improvement_rate": 12.0
        }
        
        trend_data = {
            "date": now,
            "score": 8.0,
            "curriculum_id": 123
        }
        
        score_trends_data = {
            "trends": [ScoreTrend(**trend_data)],
            "period": "week",
            "average_improvement": 3.0
        }
        
        keyword_data = {
            "keyword": "Python",
            "frequency": 10,
            "relevance_score": 8.5,
            "industry_match": True
        }
        
        data = {
            "user_metrics": ProgressMetrics(**progress_data),
            "recent_analyses": [{"id": 1, "score": 8.0}],
            "score_trends": ScoreTrendResponse(**score_trends_data),
            "top_keywords": [KeywordAnalysis(**keyword_data)],
            "recommendations": ["Melhorar layout"]
        }
        
        response = DashboardResponse(**data)
        assert response.industry_insights is None


class TestReportFilters:
    """Testa o schema ReportFilters."""
    
    def test_report_filters_valid(self):
        """Testa criação válida de ReportFilters."""
        now = datetime.now()
        data = {
            "start_date": now,
            "end_date": now,
            "min_score": 5.0,
            "max_score": 10.0,
            "industry": "Technology",
            "include_versions": True
        }
        filters = ReportFilters(**data)
        assert filters.start_date == now
        assert filters.end_date == now
        assert filters.min_score == 5.0
        assert filters.max_score == 10.0
        assert filters.industry == "Technology"
        assert filters.include_versions is True
    
    def test_report_filters_defaults(self):
        """Testa valores padrão de ReportFilters."""
        filters = ReportFilters()
        assert filters.start_date is None
        assert filters.end_date is None
        assert filters.min_score is None
        assert filters.max_score is None
        assert filters.industry is None
        assert filters.include_versions is True


class TestReportResponse:
    """Testa o schema ReportResponse."""
    
    def test_report_response_valid(self):
        """Testa criação válida de ReportResponse."""
        now = datetime.now()
        
        filters_data = {
            "start_date": now,
            "end_date": now,
            "min_score": 5.0,
            "max_score": 10.0,
            "industry": "Technology",
            "include_versions": True
        }
        
        data = {
            "generated_at": now,
            "filters": ReportFilters(**filters_data),
            "summary": {"total_analyses": 50, "average_score": 7.8},
            "detailed_data": [{"id": 1, "score": 8.5}],
            "charts_data": {"line_chart": [1, 2, 3], "bar_chart": [4, 5, 6]},
            "recommendations": ["Melhorar formatação", "Adicionar projetos"]
        }
        
        response = ReportResponse(**data)
        assert response.generated_at == now
        assert response.filters.industry == "Technology"
        assert response.summary["total_analyses"] == 50
        assert len(response.detailed_data) == 1
        assert "line_chart" in response.charts_data
        assert len(response.recommendations) == 2


class TestCurriculumMetrics:
    """Testa o schema CurriculumMetrics."""
    
    def test_curriculum_metrics_valid(self):
        """Testa criação válida de CurriculumMetrics."""
        data = {
            "score": 85.5,
            "clarity": 90.0,
            "relevance": 88.5,
            "keywords": 92.0,
            "structure": 87.5,
            "personalization": 89.0
        }
        metrics = CurriculumMetrics(**data)
        assert metrics.score == 85.5
        assert metrics.clarity == 90.0
        assert metrics.relevance == 88.5
        assert metrics.keywords == 92.0
        assert metrics.structure == 87.5
        assert metrics.personalization == 89.0
    
    def test_curriculum_metrics_score_validation(self):
        """Testa validação de pontuações (0-100)."""
        # Score válido
        valid_data = {
            "score": 50.0,
            "clarity": 75.0,
            "relevance": 80.0,
            "keywords": 85.0,
            "structure": 70.0,
            "personalization": 65.0
        }
        metrics = CurriculumMetrics(**valid_data)
        assert metrics.score == 50.0
        
        # Score inválido (menor que 0)
        invalid_data_low = {
            "score": -5.0,
            "clarity": 75.0,
            "relevance": 80.0,
            "keywords": 85.0,
            "structure": 70.0,
            "personalization": 65.0
        }
        with pytest.raises(ValidationError):
            CurriculumMetrics(**invalid_data_low)
        
        # Score inválido (maior que 100)
        invalid_data_high = {
            "score": 105.0,
            "clarity": 75.0,
            "relevance": 80.0,
            "keywords": 85.0,
            "structure": 70.0,
            "personalization": 65.0
        }
        with pytest.raises(ValidationError):
            CurriculumMetrics(**invalid_data_high)


class TestCurriculumVersionMetrics:
    """Testa o schema CurriculumVersionMetrics."""
    
    def test_curriculum_version_metrics_valid(self):
        """Testa criação válida de CurriculumVersionMetrics."""
        now = datetime.now()
        
        metrics_data = {
            "score": 85.5,
            "clarity": 90.0,
            "relevance": 88.5,
            "keywords": 92.0,
            "structure": 87.5,
            "personalization": 89.0
        }
        
        data = {
            "version_id": "v1.2.3",
            "timestamp": now,
            "metrics": CurriculumMetrics(**metrics_data)
        }
        
        version_metrics = CurriculumVersionMetrics(**data)
        assert version_metrics.version_id == "v1.2.3"
        assert version_metrics.timestamp == now
        assert version_metrics.metrics.score == 85.5


class TestTimeSeriesMetricsResponse:
    """Testa o schema TimeSeriesMetricsResponse."""
    
    def test_time_series_metrics_response_valid(self):
        """Testa criação válida de TimeSeriesMetricsResponse."""
        now = datetime.now()
        
        metrics_data = {
            "score": 85.5,
            "clarity": 90.0,
            "relevance": 88.5,
            "keywords": 92.0,
            "structure": 87.5,
            "personalization": 89.0
        }
        
        version_metrics_data = {
            "version_id": "v1.0",
            "timestamp": now,
            "metrics": CurriculumMetrics(**metrics_data)
        }
        
        data = {
            "user_id": 123,
            "total_versions": 5,
            "time_series": [CurriculumVersionMetrics(**version_metrics_data)],
            "average_score": 82.5,
            "best_score": 89.0,
            "improvement_rate": 12.5
        }
        
        response = TimeSeriesMetricsResponse(**data)
        assert response.user_id == 123
        assert response.total_versions == 5
        assert len(response.time_series) == 1
        assert response.average_score == 82.5
        assert response.best_score == 89.0
        assert response.improvement_rate == 12.5


class TestSchemaValidation:
    """Testa validações gerais dos schemas."""
    
    def test_required_fields_validation(self):
        """Testa validação de campos obrigatórios."""
        # ProgressMetrics sem campos obrigatórios
        with pytest.raises(ValidationError):
            ProgressMetrics()
        
        # ScoreTrend sem campos obrigatórios
        with pytest.raises(ValidationError):
            ScoreTrend()
        
        # CurriculumMetrics sem campos obrigatórios
        with pytest.raises(ValidationError):
            CurriculumMetrics()
    
    def test_field_types_validation(self):
        """Testa validação de tipos de campos."""
        now = datetime.now()
        
        # total_curriculum deve ser int
        with pytest.raises(ValidationError):
            ProgressMetrics(
                total_curriculum="not_an_int",
                total_analyses=6,
                average_score=8.0,
                best_score=9.0,
                improvement_rate=12.0
            )
        
        # average_score deve ser float
        with pytest.raises(ValidationError):
            ProgressMetrics(
                total_curriculum=3,
                total_analyses=6,
                average_score="not_a_float",
                best_score=9.0,
                improvement_rate=12.0
            )
    
    def test_nested_schema_validation(self):
        """Testa validação de schemas aninhados."""
        # CurriculumMetrics inválido dentro de CurriculumVersionMetrics
        invalid_metrics = {"score": "not_a_number"}
        
        with pytest.raises(ValidationError):
            CurriculumMetrics(**invalid_metrics)
    
    def test_field_constraints_validation(self):
        """Testa validação de restrições de campos."""
        # Score deve estar entre 0 e 100
        with pytest.raises(ValidationError):
            CurriculumMetrics(
                score=150.0,  # Maior que 100
                clarity=75.0,
                relevance=80.0,
                keywords=85.0,
                structure=70.0,
                personalization=65.0
            )
        
        with pytest.raises(ValidationError):
            CurriculumMetrics(
                score=-10.0,  # Menor que 0
                clarity=75.0,
                relevance=80.0,
                keywords=85.0,
                structure=70.0,
                personalization=65.0
            )


class TestSchemaEdgeCases:
    """Testa casos extremos dos schemas."""
    
    def test_empty_lists_validation(self):
        """Testa validação de listas vazias."""
        # DashboardResponse com listas vazias
        now = datetime.now()
        
        progress_data = {
            "total_curriculum": 0,
            "total_analyses": 0,
            "average_score": 0.0,
            "best_score": 0.0,
            "improvement_rate": 0.0
        }
        
        trend_data = {
            "date": now,
            "score": 0.0,
            "curriculum_id": 123
        }
        
        score_trends_data = {
            "trends": [],
            "period": "week",
            "average_improvement": 0.0
        }
        
        data = {
            "user_metrics": ProgressMetrics(**progress_data),
            "recent_analyses": [],
            "score_trends": ScoreTrendResponse(**score_trends_data),
            "top_keywords": [],
            "recommendations": []
        }
        
        response = DashboardResponse(**data)
        assert response.recent_analyses == []
        assert response.top_keywords == []
        assert response.recommendations == []
    
    def test_none_values_validation(self):
        """Testa validação de valores None."""
        # ReportFilters com campos opcionais None
        filters = ReportFilters()
        assert filters.start_date is None
        assert filters.end_date is None
        assert filters.min_score is None
        assert filters.max_score is None
        assert filters.industry is None
    
    def test_large_values_validation(self):
        """Testa validação de valores grandes."""
        # Valores grandes mas válidos
        now = datetime.now()
        
        progress_data = {
            "total_curriculum": 999999,
            "total_analyses": 999999,
            "average_score": 99.99,
            "best_score": 99.99,
            "improvement_rate": 999.99
        }
        
        metrics = ProgressMetrics(**progress_data)
        assert metrics.total_curriculum == 999999
        assert metrics.total_analyses == 999999
        assert metrics.average_score == 99.99
        assert metrics.best_score == 99.99
        assert metrics.improvement_rate == 999.99


class TestSchemaInheritance:
    """Testa herança entre schemas."""
    
    def test_all_schemas_inherit_base_model(self):
        """Testa se todos os schemas herdam de BaseModel."""
        schemas = [
            ProgressMetrics, ScoreTrend, ScoreTrendResponse,
            KeywordAnalysis, IndustryInsights, ComparativeAnalysis,
            DashboardResponse, ReportFilters, ReportResponse,
            CurriculumMetrics, CurriculumVersionMetrics, TimeSeriesMetricsResponse
        ]
        
        for schema in schemas:
            assert hasattr(schema, 'model_fields')  # Indica que é um Pydantic model


class TestSchemaDescriptions:
    """Testa descrições dos campos."""
    
    def test_field_descriptions(self):
        """Testa se os campos têm descrições quando especificadas."""
        # CurriculumMetrics tem descrições nos campos
        score_field = CurriculumMetrics.model_fields['score']
        assert hasattr(score_field, 'description')
        assert score_field.description == "Pontuação geral (0-100)"
        
        clarity_field = CurriculumMetrics.model_fields['clarity']
        assert hasattr(clarity_field, 'description')
        assert clarity_field.description == "Clareza textual (0-100)"
        
        # CurriculumVersionMetrics tem descrições nos campos
        version_id_field = CurriculumVersionMetrics.model_fields['version_id']
        assert hasattr(version_id_field, 'description')
        assert version_id_field.description == "Identificador da versão"
        
        timestamp_field = CurriculumVersionMetrics.model_fields['timestamp']
        assert hasattr(timestamp_field, 'description')
        assert timestamp_field.description == "Data/hora do envio"
