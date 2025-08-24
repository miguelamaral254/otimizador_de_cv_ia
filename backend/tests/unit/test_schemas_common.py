"""
Testes unitários para schemas comuns.
"""

import pytest
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ValidationError, Field
from app.schemas.common import (
    MessageResponse,
    ErrorResponse,
    ValidationErrorResponse,
    PaginationParams,
    PaginationResponse,
    PaginatedResponse,
    HealthCheckResponse,
    FileUploadResponse,
    SearchResponse
)


class TestMessageResponse:
    """Testes para o schema MessageResponse."""
    
    def test_message_response_inheritance(self):
        """Testa se MessageResponse herda de BaseModel."""
        assert issubclass(MessageResponse, BaseModel)
    
    def test_message_response_instantiation(self):
        """Testa instanciação do MessageResponse."""
        schema = MessageResponse(message="Teste")
        assert isinstance(schema, MessageResponse)
        assert isinstance(schema, BaseModel)
    
    def test_message_response_fields(self):
        """Testa campos do MessageResponse."""
        schema = MessageResponse(message="Teste")
        
        # Verifica se os campos existem
        assert hasattr(schema, 'message')
        assert hasattr(schema, 'timestamp')
    
    def test_message_response_default_values(self):
        """Testa valores padrão do MessageResponse."""
        schema = MessageResponse(message="Teste")
        
        # Verifica valores padrão
        assert schema.message == "Teste"
        assert schema.timestamp is not None
        assert isinstance(schema.timestamp, datetime)
    
    def test_message_response_custom_values(self):
        """Testa MessageResponse com valores customizados."""
        custom_time = datetime(2023, 1, 1, 12, 0, 0)
        data = {
            "message": "Mensagem customizada",
            "timestamp": custom_time
        }
        
        schema = MessageResponse(**data)
        
        assert schema.message == "Mensagem customizada"
        assert schema.timestamp == custom_time
    
    def test_message_response_validation(self):
        """Testa validação do MessageResponse."""
        # Dados válidos
        valid_data = {"message": "Mensagem válida"}
        schema = MessageResponse(**valid_data)
        assert schema.message == "Mensagem válida"
        
        # Dados inválidos
        invalid_data = {"message": 123}  # message deve ser string
        with pytest.raises(ValidationError):
            MessageResponse(**invalid_data)
    
    def test_message_response_timestamp_auto(self):
        """Testa se o timestamp é definido automaticamente."""
        schema = MessageResponse(message="Teste")
        
        # Timestamp deve ser definido automaticamente
        assert schema.timestamp is not None
        assert isinstance(schema.timestamp, datetime)
        
        # Deve ser um timestamp recente
        now = datetime.utcnow()
        time_diff = abs((now - schema.timestamp).total_seconds())
        assert time_diff < 10  # Deve ser criado nos últimos 10 segundos


class TestErrorResponse:
    """Testes para o schema ErrorResponse."""
    
    def test_error_response_inheritance(self):
        """Testa se ErrorResponse herda de BaseModel."""
        assert issubclass(ErrorResponse, BaseModel)
    
    def test_error_response_fields(self):
        """Testa campos do ErrorResponse."""
        schema = ErrorResponse(error="Erro teste")
        
        # Verifica se os campos existem
        assert hasattr(schema, 'error')
        assert hasattr(schema, 'detail')
        assert hasattr(schema, 'timestamp')
        assert hasattr(schema, 'error_code')
    
    def test_error_response_default_values(self):
        """Testa valores padrão do ErrorResponse."""
        schema = ErrorResponse(error="Erro teste")
        
        # Verifica valores padrão
        assert schema.error == "Erro teste"
        assert schema.detail is None
        assert schema.timestamp is not None
        assert schema.error_code is None
    
    def test_error_response_custom_values(self):
        """Testa ErrorResponse com valores customizados."""
        custom_time = datetime(2023, 1, 1, 12, 0, 0)
        data = {
            "error": "Erro customizado",
            "detail": "Detalhes do erro",
            "timestamp": custom_time,
            "error_code": "ERR_001"
        }
        
        schema = ErrorResponse(**data)
        
        assert schema.error == "Erro customizado"
        assert schema.detail == "Detalhes do erro"
        assert schema.timestamp == custom_time
        assert schema.error_code == "ERR_001"
    
    def test_error_response_validation(self):
        """Testa validação do ErrorResponse."""
        # Dados válidos
        valid_data = {
            "error": "Erro válido",
            "detail": "Detalhes válidos",
            "error_code": "CODE_001"
        }
        schema = ErrorResponse(**valid_data)
        assert schema.error == "Erro válido"
        assert schema.detail == "Detalhes válidos"
        assert schema.error_code == "CODE_001"
        
        # Dados inválidos
        invalid_data = {
            "error": 123,  # error deve ser string
            "detail": ["não é string"],  # detail deve ser string
            "error_code": 456  # error_code deve ser string
        }
        with pytest.raises(ValidationError):
            ErrorResponse(**invalid_data)


class TestValidationErrorResponse:
    """Testes para o schema ValidationErrorResponse."""
    
    def test_validation_error_response_inheritance(self):
        """Testa se ValidationErrorResponse herda de BaseModel."""
        assert issubclass(ValidationErrorResponse, BaseModel)
    
    def test_validation_error_response_fields(self):
        """Testa campos do ValidationErrorResponse."""
        schema = ValidationErrorResponse()
        
        # Verifica se os campos existem
        assert hasattr(schema, 'error')
        assert hasattr(schema, 'detail')
        assert hasattr(schema, 'timestamp')
    
    def test_validation_error_response_default_values(self):
        """Testa valores padrão do ValidationErrorResponse."""
        schema = ValidationErrorResponse()
        
        # Verifica valores padrão
        assert schema.error == "Erro de validação"
        assert schema.detail == []
        assert schema.timestamp is not None
        assert isinstance(schema.timestamp, datetime)
    
    def test_validation_error_response_custom_values(self):
        """Testa ValidationErrorResponse com valores customizados."""
        custom_time = datetime(2023, 1, 1, 12, 0, 0)
        data = {
            "error": "Erro de validação customizado",
            "detail": [{"field": "email", "error": "Email inválido"}],
            "timestamp": custom_time
        }
        
        schema = ValidationErrorResponse(**data)
        
        assert schema.error == "Erro de validação customizado"
        assert len(schema.detail) == 1
        assert schema.detail[0]["field"] == "email"
        assert schema.timestamp == custom_time


class TestPaginationParams:
    """Testes para o schema PaginationParams."""
    
    def test_pagination_params_inheritance(self):
        """Testa se PaginationParams herda de BaseModel."""
        assert issubclass(PaginationParams, BaseModel)
    
    def test_pagination_params_fields(self):
        """Testa campos do PaginationParams."""
        schema = PaginationParams()
        
        # Verifica se os campos existem
        assert hasattr(schema, 'page')
        assert hasattr(schema, 'per_page')
        assert hasattr(schema, 'sort_by')
        assert hasattr(schema, 'sort_order')
    
    def test_pagination_params_default_values(self):
        """Testa valores padrão do PaginationParams."""
        schema = PaginationParams()
        
        # Verifica valores padrão
        assert schema.page == 1
        assert schema.per_page == 10
        assert schema.sort_by is None
        assert schema.sort_order == "desc"
    
    def test_pagination_params_custom_values(self):
        """Testa PaginationParams com valores customizados."""
        data = {
            "page": 5,
            "per_page": 25,
            "sort_by": "created_at",
            "sort_order": "asc"
        }
        
        schema = PaginationParams(**data)
        
        assert schema.page == 5
        assert schema.per_page == 25
        assert schema.sort_by == "created_at"
        assert schema.sort_order == "asc"
    
    def test_pagination_params_validation(self):
        """Testa validação do PaginationParams."""
        # Dados válidos
        valid_data = {
            "page": 1,
            "per_page": 20,
            "sort_by": "name",
            "sort_order": "desc"
        }
        schema = PaginationParams(**valid_data)
        assert schema.page == 1
        assert schema.per_page == 20
        
        # Dados inválidos
        invalid_data = {
            "page": 0,  # Página deve ser >= 1
            "per_page": 0,  # Tamanho deve ser >= 1
            "sort_order": "invalid"  # Deve ser asc ou desc
        }
        with pytest.raises(ValidationError):
            PaginationParams(**invalid_data)
    
    def test_pagination_params_sort_order_pattern(self):
        """Testa padrão do campo sort_order."""
        # Valores válidos
        valid_orders = ["asc", "desc"]
        for order in valid_orders:
            schema = PaginationParams(sort_order=order)
            assert schema.sort_order == order
        
        # Valores inválidos
        invalid_orders = ["ASC", "DESC", "up", "down", "invalid"]
        for order in invalid_orders:
            with pytest.raises(ValidationError):
                PaginationParams(sort_order=order)


class TestPaginationResponse:
    """Testes para o schema PaginationResponse."""
    
    def test_pagination_response_inheritance(self):
        """Testa se PaginationResponse herda de BaseModel."""
        assert issubclass(PaginationResponse, BaseModel)
    
    def test_pagination_response_fields(self):
        """Testa campos do PaginationResponse."""
        schema = PaginationResponse(
            page=1,
            per_page=10,
            total=100,
            total_pages=10,
            has_next=True,
            has_prev=False
        )
        
        # Verifica se os campos existem
        assert hasattr(schema, 'page')
        assert hasattr(schema, 'per_page')
        assert hasattr(schema, 'total')
        assert hasattr(schema, 'total_pages')
        assert hasattr(schema, 'has_next')
        assert hasattr(schema, 'has_prev')
    
    def test_pagination_response_values(self):
        """Testa valores do PaginationResponse."""
        data = {
            "page": 2,
            "per_page": 20,
            "total": 150,
            "total_pages": 8,
            "has_next": True,
            "has_prev": True
        }
        
        schema = PaginationResponse(**data)
        
        assert schema.page == 2
        assert schema.per_page == 20
        assert schema.total == 150
        assert schema.total_pages == 8
        assert schema.has_next is True
        assert schema.has_prev is True
    
    def test_pagination_response_validation(self):
        """Testa validação do PaginationResponse."""
        # Dados válidos
        valid_data = {
            "page": 1,
            "per_page": 10,
            "total": 0,
            "total_pages": 0,
            "has_next": False,
            "has_prev": False
        }
        schema = PaginationResponse(**valid_data)
        assert schema.page == 1
        assert schema.total == 0
        
        # Dados inválidos
        invalid_data = {
            "page": "não é número",  # page deve ser int
            "per_page": 10,
            "total": 100,
            "total_pages": 10,
            "has_next": "não é boolean",  # has_next deve ser boolean
            "has_prev": False
        }
        with pytest.raises(ValidationError):
            PaginationResponse(**invalid_data)


class TestPaginatedResponse:
    """Testes para o schema PaginatedResponse."""
    
    def test_paginated_response_inheritance(self):
        """Testa se PaginatedResponse herda de BaseModel."""
        assert issubclass(PaginatedResponse, BaseModel)
    
    def test_paginated_response_generic(self):
        """Testa se PaginatedResponse é genérico."""
        # Verifica se funciona como genérico
        try:
            paginated_str = PaginatedResponse[str]
            assert paginated_str is not None
            assert str(paginated_str) != str(PaginatedResponse)
        except TypeError:
            pytest.fail("PaginatedResponse deveria ser genérico")
        
        # Verifica se funciona como esperado
        assert hasattr(PaginatedResponse, '__class_getitem__')
    
    def test_paginated_response_fields(self):
        """Testa campos do PaginatedResponse."""
        # Cria um schema de exemplo
        class ItemSchema(BaseModel):
            id: int
            name: str
        
        pagination = PaginationResponse(
            page=1,
            per_page=10,
            total=50,
            total_pages=5,
            has_next=True,
            has_prev=False
        )
        
        items = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"}
        ]
        
        schema = PaginatedResponse[ItemSchema](
            data=items,
            pagination=pagination
        )
        
        # Verifica se os campos existem
        assert hasattr(schema, 'data')
        assert hasattr(schema, 'pagination')
        
        assert len(schema.data) == 2
        assert schema.data[0].id == 1
        assert schema.data[1].name == "Item 2"
        assert schema.pagination.page == 1


class TestHealthCheckResponse:
    """Testes para o schema HealthCheckResponse."""
    
    def test_health_check_response_inheritance(self):
        """Testa se HealthCheckResponse herda de BaseModel."""
        assert issubclass(HealthCheckResponse, BaseModel)
    
    def test_health_check_response_fields(self):
        """Testa campos do HealthCheckResponse."""
        schema = HealthCheckResponse(
            status="healthy",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            environment="development",
            database_status="connected",
            ai_services_status={"gemini": "active", "spacy": "active"}
        )
        
        # Verifica se os campos existem
        assert hasattr(schema, 'status')
        assert hasattr(schema, 'timestamp')
        assert hasattr(schema, 'version')
        assert hasattr(schema, 'environment')
        assert hasattr(schema, 'database_status')
        assert hasattr(schema, 'ai_services_status')
    
    def test_health_check_response_values(self):
        """Testa valores do HealthCheckResponse."""
        custom_time = datetime(2023, 1, 1, 12, 0, 0)
        data = {
            "status": "degraded",
            "timestamp": custom_time,
            "version": "2.1.0",
            "environment": "production",
            "database_status": "slow",
            "ai_services_status": {"gemini": "active", "spacy": "inactive"}
        }
        
        schema = HealthCheckResponse(**data)
        
        assert schema.status == "degraded"
        assert schema.timestamp == custom_time
        assert schema.version == "2.1.0"
        assert schema.environment == "production"
        assert schema.database_status == "slow"
        assert schema.ai_services_status["spacy"] == "inactive"


class TestFileUploadResponse:
    """Testes para o schema FileUploadResponse."""
    
    def test_file_upload_response_inheritance(self):
        """Testa se FileUploadResponse herda de BaseModel."""
        assert issubclass(FileUploadResponse, BaseModel)
    
    def test_file_upload_response_fields(self):
        """Testa campos do FileUploadResponse."""
        schema = FileUploadResponse(
            filename="test.pdf",
            file_path="/uploads/test.pdf",
            file_size=1024,
            content_type="application/pdf",
            upload_time=datetime.utcnow()
        )
        
        # Verifica se os campos existem
        assert hasattr(schema, 'filename')
        assert hasattr(schema, 'file_path')
        assert hasattr(schema, 'file_size')
        assert hasattr(schema, 'content_type')
        assert hasattr(schema, 'upload_time')
        assert hasattr(schema, 'message')
    
    def test_file_upload_response_default_message(self):
        """Testa mensagem padrão do FileUploadResponse."""
        schema = FileUploadResponse(
            filename="test.pdf",
            file_path="/uploads/test.pdf",
            file_size=1024,
            content_type="application/pdf",
            upload_time=datetime.utcnow()
        )
        
        assert schema.message == "Arquivo enviado com sucesso!"
    
    def test_file_upload_response_custom_message(self):
        """Testa mensagem customizada do FileUploadResponse."""
        data = {
            "filename": "test.pdf",
            "file_path": "/uploads/test.pdf",
            "file_size": 1024,
            "content_type": "application/pdf",
            "upload_time": datetime.utcnow(),
            "message": "Arquivo processado com sucesso!"
        }
        
        schema = FileUploadResponse(**data)
        
        assert schema.message == "Arquivo processado com sucesso!"


class TestSearchResponse:
    """Testes para o schema SearchResponse."""
    
    def test_search_response_inheritance(self):
        """Testa se SearchResponse herda de BaseModel."""
        assert issubclass(SearchResponse, BaseModel)
    
    def test_search_response_fields(self):
        """Testa campos do SearchResponse."""
        schema = SearchResponse(
            query="python developer",
            results=[{"id": 1, "name": "João"}],
            total_results=1,
            search_time=0.5
        )
        
        # Verifica se os campos existem
        assert hasattr(schema, 'query')
        assert hasattr(schema, 'results')
        assert hasattr(schema, 'total_results')
        assert hasattr(schema, 'search_time')
        assert hasattr(schema, 'filters_applied')
    
    def test_search_response_default_filters(self):
        """Testa filtros padrão do SearchResponse."""
        schema = SearchResponse(
            query="test",
            results=[],
            total_results=0,
            search_time=0.1
        )
        
        assert schema.filters_applied == {}
    
    def test_search_response_custom_filters(self):
        """Testa filtros customizados do SearchResponse."""
        data = {
            "query": "python",
            "results": [],
            "total_results": 0,
            "search_time": 0.2,
            "filters_applied": {
                "location": "São Paulo",
                "experience": "senior",
                "skills": ["python", "django"]
            }
        }
        
        schema = SearchResponse(**data)
        
        assert schema.filters_applied["location"] == "São Paulo"
        assert schema.filters_applied["experience"] == "senior"
        assert "python" in schema.filters_applied["skills"]


class TestSchemaIntegration:
    """Testes de integração entre schemas."""
    
    def test_pagination_integration(self):
        """Testa integração entre schemas de paginação."""
        # Cria parâmetros de paginação
        params = PaginationParams(
            page=2,
            per_page=15,
            sort_by="created_at",
            sort_order="desc"
        )
        
        # Cria resposta de paginação
        pagination = PaginationResponse(
            page=2,
            per_page=15,
            total=45,
            total_pages=3,
            has_next=True,
            has_prev=True
        )
        
        # Verifica integração
        assert params.page == pagination.page
        assert params.per_page == pagination.per_page
        assert pagination.has_next is True
        assert pagination.has_prev is True
    
    def test_error_integration(self):
        """Testa integração entre schemas de erro."""
        # Cria erro de validação
        validation_error = ValidationErrorResponse(
            detail=[{"field": "email", "error": "Email inválido"}]
        )
        
        # Cria resposta de erro
        error_response = ErrorResponse(
            error="Erro de validação",
            detail="Verifique os campos obrigatórios",
            error_code="VAL_001"
        )
        
        # Verifica integração
        assert validation_error.error == "Erro de validação"
        assert error_response.error_code == "VAL_001"
        assert len(validation_error.detail) == 1


class TestSchemaEdgeCases:
    """Testes para casos extremos dos schemas."""
    
    def test_empty_strings(self):
        """Testa schemas com strings vazias."""
        # MessageResponse com mensagem vazia
        schema = MessageResponse(message="")
        assert schema.message == ""
        
        # ErrorResponse com erro vazio
        schema = ErrorResponse(error="")
        assert schema.error == ""
    
    def test_very_long_strings(self):
        """Testa schemas com strings muito longas."""
        long_string = "a" * 1000
        
        # MessageResponse com mensagem longa
        schema = MessageResponse(message=long_string)
        assert len(schema.message) == 1000
        
        # ErrorResponse com erro longo
        schema = ErrorResponse(error=long_string)
        assert len(schema.error) == 1000
    
    def test_special_characters(self):
        """Testa schemas com caracteres especiais."""
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?\"'\\`~"
        unicode_chars = "áéíóúâêîôûãõçñÁÉÍÓÚÂÊÎÔÛÃÕÇÑ"
        emojis = "🚀💻📚🎯✨🔥"
        
        # MessageResponse com caracteres especiais
        schema = MessageResponse(message=f"{special_chars} {unicode_chars} {emojis}")
        assert special_chars in schema.message
        assert unicode_chars in schema.message
        assert emojis in schema.message
    
    def test_nested_structures(self):
        """Testa schemas com estruturas aninhadas complexas."""
        # SearchResponse com filtros complexos
        complex_filters = {
            "user": {
                "profile": {
                    "skills": ["python", "react", "docker"],
                    "experience": {
                        "min": 2,
                        "max": 10
                    }
                },
                "preferences": {
                    "remote": True,
                    "salary_range": [5000, 15000]
                }
            },
            "company": {
                "size": "medium",
                "industry": "technology"
            }
        }
        
        schema = SearchResponse(
            query="full stack developer",
            results=[],
            total_results=0,
            search_time=0.3,
            filters_applied=complex_filters
        )
        
        assert schema.filters_applied["user"]["profile"]["skills"] == ["python", "react", "docker"]
        assert schema.filters_applied["user"]["preferences"]["remote"] is True
        assert schema.filters_applied["company"]["size"] == "medium"
