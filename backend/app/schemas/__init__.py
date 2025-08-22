from .user import UserCreate, UserUpdate, UserResponse, UserLogin, Token, TokenData
from .curriculum import (
    CurriculumCreate, 
    CurriculumUpdate, 
    CurriculumResponse,
    CurriculumVersionCreate,
    CurriculumVersionResponse,
    CurriculumAnalysisResponse,
    CurriculumUploadResponse,
    CurriculumListResponse,
    CurriculumWithAnalysisResponse
)
from .metrics import (
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

__all__ = [
    # User schemas
    "UserCreate", "UserUpdate", "UserResponse", "UserLogin", "Token", "TokenData",
    # Curriculum schemas
    "CurriculumCreate", "CurriculumUpdate", "CurriculumResponse",
    "CurriculumVersionCreate", "CurriculumVersionResponse",
    "CurriculumAnalysisResponse", "CurriculumUploadResponse",
    "CurriculumListResponse", "CurriculumWithAnalysisResponse",
    # Metrics schemas
    "ProgressMetrics", "ScoreTrend", "ScoreTrendResponse", "KeywordAnalysis",
    "IndustryInsights", "ComparativeAnalysis", "DashboardResponse",
    "ReportFilters", "ReportResponse", "CurriculumMetrics", "CurriculumVersionMetrics",
    "TimeSeriesMetricsResponse"
]
