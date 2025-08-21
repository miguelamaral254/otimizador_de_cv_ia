from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, List, Any, Dict
from datetime import datetime


class MessageResponse(BaseModel):
    """Schema para respostas de mensagem simples."""
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Schema para respostas de erro."""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error_code: Optional[str] = None


class ValidationErrorResponse(BaseModel):
    """Schema para erros de validação."""
    error: str = "Erro de validação"
    detail: List[dict] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PaginationParams(BaseModel):
    """Schema para parâmetros de paginação."""
    page: int = Field(1, ge=1, description="Número da página")
    per_page: int = Field(10, ge=1, le=100, description="Itens por página")
    sort_by: Optional[str] = None
    sort_order: str = Field("desc", regex="^(asc|desc)$")


class PaginationResponse(BaseModel):
    """Schema para resposta de paginação."""
    page: int
    per_page: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool


T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Schema genérico para respostas paginadas."""
    data: List[T]
    pagination: PaginationResponse


class HealthCheckResponse(BaseModel):
    """Schema para health check da API."""
    status: str
    timestamp: datetime
    version: str
    environment: str
    database_status: str
    ai_services_status: Dict[str, str]


class FileUploadResponse(BaseModel):
    """Schema para resposta de upload de arquivo."""
    filename: str
    file_path: str
    file_size: int
    content_type: str
    upload_time: datetime
    message: str = "Arquivo enviado com sucesso!"


class SearchResponse(BaseModel):
    """Schema para respostas de busca."""
    query: str
    results: List[Any]
    total_results: int
    search_time: float  # Tempo de busca em segundos
    filters_applied: Dict[str, Any] = {}
