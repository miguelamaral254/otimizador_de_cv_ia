from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class CurriculumBase(BaseModel):
    """Schema base para currículos."""
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None


class CurriculumCreate(CurriculumBase):
    """Schema para criação de currículo."""
    user_id: int
    original_filename: str
    file_path: str
    file_size: int


class CurriculumUpdate(CurriculumBase):
    """Schema para atualização de currículo."""
    pass


class CurriculumResponse(CurriculumBase):
    """Schema para resposta de currículo."""
    id: int
    user_id: int
    original_filename: str
    file_path: str
    file_size: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CurriculumVersionCreate(BaseModel):
    """Schema para criação de versão de currículo."""
    version_name: Optional[str] = Field(None, max_length=100)
    changes_description: Optional[str] = None


class CurriculumVersionResponse(CurriculumVersionCreate):
    """Schema para resposta de versão de currículo."""
    id: int
    curriculum_id: int
    version_number: int
    file_path: str
    file_size: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SpacyAnalysis(BaseModel):
    """Schema para análise do spaCy."""
    action_verbs: List[str] = []
    quantified_results: List[str] = []
    keywords_found: List[str] = []
    text_statistics: Dict[str, Any] = {}


class GeminiAnalysis(BaseModel):
    """Schema para análise do Google Gemini."""
    overall_assessment: str
    strengths: List[str] = []
    weaknesses: List[str] = []
    suggestions: List[str] = []
    industry_relevance: str
    improvement_areas: List[str] = []


class CurriculumAnalysisResponse(BaseModel):
    """Schema para resposta de análise de currículo."""
    id: int
    curriculum_id: int
    version_id: Optional[int] = None
    
    # Análises
    spacy_analysis: Optional[SpacyAnalysis] = None
    gemini_analysis: Optional[GeminiAnalysis] = None
    
    # Métricas quantitativas
    action_verbs_count: int
    quantified_results_count: int
    keywords_score: float
    overall_score: float
    
    # Feedback da IA
    strengths: List[str] = []
    weaknesses: List[str] = []
    suggestions: List[str] = []
    
    # Metadados
    analysis_date: datetime
    processing_time: Optional[float] = None
    
    class Config:
        from_attributes = True


class CurriculumUploadResponse(BaseModel):
    """Schema para resposta de upload de currículo."""
    curriculum: CurriculumResponse
    analysis: Optional[CurriculumAnalysisResponse] = None
    message: str = "Currículo enviado com sucesso!"


class CurriculumListResponse(BaseModel):
    """Schema para lista de currículos."""
    curricula: List[CurriculumResponse]
    total: int
    page: int
    per_page: int


class CurriculumWithAnalysisResponse(BaseModel):
    """Schema para currículo com análise completa."""
    curriculum: CurriculumResponse
    latest_analysis: Optional[CurriculumAnalysisResponse] = None
    versions: List[CurriculumVersionResponse] = []
    analysis_history: List[CurriculumAnalysisResponse] = []


# --- Novos Schemas para a API de Análise ---

class CurriculumInfo(BaseModel):
    """Schema para informações básicas do currículo."""
    id: int
    user_id: int
    filename: str
    file_path: str
    upload_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CurriculumAnalysis(BaseModel):
    """Schema principal para a resposta completa da análise."""
    curriculum_info: CurriculumInfo
    analysis: Dict[str, Any]
