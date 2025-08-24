"""
Testes unitários para app/schemas/curriculum.py
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.curriculum import (
    CurriculumBase,
    CurriculumCreate,
    CurriculumUpdate,
    CurriculumResponse,
    CurriculumVersionCreate,
    CurriculumVersionResponse,
    SpacyAnalysis,
    GeminiAnalysis,
    CurriculumAnalysisResponse,
    CurriculumUploadResponse,
    CurriculumListResponse,
    CurriculumWithAnalysisResponse,
    CurriculumInfo,
    CurriculumAnalysis
)


class TestCurriculumBase:
    """Testa o schema base CurriculumBase."""
    
    def test_curriculum_base_valid(self):
        """Testa criação válida de CurriculumBase."""
        data = {
            "title": "Desenvolvedor Python",
            "description": "Currículo para vaga de desenvolvedor"
        }
        curriculum = CurriculumBase(**data)
        assert curriculum.title == "Desenvolvedor Python"
        assert curriculum.description == "Currículo para vaga de desenvolvedor"
    
    def test_curriculum_base_optional_fields(self):
        """Testa criação com campos opcionais."""
        curriculum = CurriculumBase()
        assert curriculum.title is None
        assert curriculum.description is None
    
    def test_curriculum_base_title_max_length(self):
        """Testa limite máximo do título."""
        long_title = "a" * 201
        with pytest.raises(ValidationError):
            CurriculumBase(title=long_title)


class TestCurriculumCreate:
    """Testa o schema CurriculumCreate."""
    
    def test_curriculum_create_inheritance(self):
        """Testa se herda corretamente de CurriculumBase."""
        data = {"title": "Teste"}
        curriculum = CurriculumCreate(**data)
        assert isinstance(curriculum, CurriculumBase)
        assert curriculum.title == "Teste"


class TestCurriculumUpdate:
    """Testa o schema CurriculumUpdate."""
    
    def test_curriculum_update_inheritance(self):
        """Testa se herda corretamente de CurriculumBase."""
        data = {"description": "Nova descrição"}
        curriculum = CurriculumUpdate(**data)
        assert isinstance(curriculum, CurriculumBase)
        assert curriculum.description == "Nova descrição"


class TestCurriculumResponse:
    """Testa o schema CurriculumResponse."""
    
    def test_curriculum_response_valid(self):
        """Testa criação válida de CurriculumResponse."""
        now = datetime.now()
        data = {
            "id": 1,
            "user_id": 123,
            "original_filename": "cv.pdf",
            "file_path": "/uploads/cv.pdf",
            "file_size": 1024,
            "created_at": now,
            "updated_at": None,
            "title": "Desenvolvedor",
            "description": "Currículo"
        }
        curriculum = CurriculumResponse(**data)
        assert curriculum.id == 1
        assert curriculum.user_id == 123
        assert curriculum.original_filename == "cv.pdf"
        assert curriculum.file_size == 1024
        assert curriculum.created_at == now
    
    def test_curriculum_response_required_fields(self):
        """Testa campos obrigatórios."""
        now = datetime.now()
        data = {
            "id": 1,
            "user_id": 123,
            "original_filename": "cv.pdf",
            "file_path": "/uploads/cv.pdf",
            "file_size": 1024,
            "created_at": now
        }
        curriculum = CurriculumResponse(**data)
        assert curriculum.updated_at is None
        assert curriculum.title is None
        assert curriculum.description is None


class TestCurriculumVersionCreate:
    """Testa o schema CurriculumVersionCreate."""
    
    def test_curriculum_version_create_valid(self):
        """Testa criação válida de CurriculumVersionCreate."""
        data = {
            "version_name": "Versão 2.0",
            "changes_description": "Atualizações importantes"
        }
        version = CurriculumVersionCreate(**data)
        assert version.version_name == "Versão 2.0"
        assert version.changes_description == "Atualizações importantes"
    
    def test_curriculum_version_create_optional_fields(self):
        """Testa criação com campos opcionais."""
        version = CurriculumVersionCreate()
        assert version.version_name is None
        assert version.changes_description is None
    
    def test_curriculum_version_create_name_max_length(self):
        """Testa limite máximo do nome da versão."""
        long_name = "a" * 101
        with pytest.raises(ValidationError):
            CurriculumVersionCreate(version_name=long_name)


class TestCurriculumVersionResponse:
    """Testa o schema CurriculumVersionResponse."""
    
    def test_curriculum_version_response_valid(self):
        """Testa criação válida de CurriculumVersionResponse."""
        now = datetime.now()
        data = {
            "id": 1,
            "curriculum_id": 123,
            "version_number": 2,
            "file_path": "/uploads/cv_v2.pdf",
            "file_size": 2048,
            "created_at": now,
            "version_name": "Versão 2.0",
            "changes_description": "Atualizações"
        }
        version = CurriculumVersionResponse(**data)
        assert version.id == 1
        assert version.curriculum_id == 123
        assert version.version_number == 2
        assert version.file_size == 2048


class TestSpacyAnalysis:
    """Testa o schema SpacyAnalysis."""
    
    def test_spacy_analysis_valid(self):
        """Testa criação válida de SpacyAnalysis."""
        data = {
            "action_verbs": ["desenvolveu", "implementou"],
            "quantified_results": ["5 projetos", "3 anos"],
            "keywords_found": ["Python", "Django"],
            "text_statistics": {"word_count": 500, "sentence_count": 25}
        }
        analysis = SpacyAnalysis(**data)
        assert len(analysis.action_verbs) == 2
        assert len(analysis.quantified_results) == 2
        assert len(analysis.keywords_found) == 2
        assert analysis.text_statistics["word_count"] == 500
    
    def test_spacy_analysis_defaults(self):
        """Testa valores padrão de SpacyAnalysis."""
        analysis = SpacyAnalysis()
        assert analysis.action_verbs == []
        assert analysis.quantified_results == []
        assert analysis.keywords_found == []
        assert analysis.text_statistics == {}


class TestGeminiAnalysis:
    """Testa o schema GeminiAnalysis."""
    
    def test_gemini_analysis_valid(self):
        """Testa criação válida de GeminiAnalysis."""
        data = {
            "overall_assessment": "Excelente currículo",
            "strengths": ["Experiência sólida", "Tecnologias relevantes"],
            "weaknesses": ["Pode melhorar a formatação"],
            "suggestions": ["Adicionar projetos pessoais"],
            "industry_relevance": "Alta relevância para o mercado",
            "improvement_areas": ["Comunicação", "Liderança"]
        }
        analysis = GeminiAnalysis(**data)
        assert analysis.overall_assessment == "Excelente currículo"
        assert len(analysis.strengths) == 2
        assert len(analysis.weaknesses) == 1
        assert len(analysis.suggestions) == 1
        assert analysis.industry_relevance == "Alta relevância para o mercado"
        assert len(analysis.improvement_areas) == 2
    
    def test_gemini_analysis_defaults(self):
        """Testa valores padrão de GeminiAnalysis."""
        analysis = GeminiAnalysis(overall_assessment="Teste", industry_relevance="")
        assert analysis.overall_assessment == "Teste"
        assert analysis.strengths == []
        assert analysis.weaknesses == []
        assert analysis.suggestions == []
        assert analysis.industry_relevance == ""
        assert analysis.improvement_areas == []


class TestCurriculumAnalysisResponse:
    """Testa o schema CurriculumAnalysisResponse."""
    
    def test_curriculum_analysis_response_valid(self):
        """Testa criação válida de CurriculumAnalysisResponse."""
        now = datetime.now()
        spacy_data = {
            "action_verbs": ["desenvolveu"],
            "quantified_results": ["5 projetos"],
            "keywords_found": ["Python"],
            "text_statistics": {"word_count": 500}
        }
        gemini_data = {
            "overall_assessment": "Bom currículo",
            "strengths": ["Experiência"],
            "weaknesses": [],
            "suggestions": [],
            "industry_relevance": "",
            "improvement_areas": []
        }
        
        data = {
            "id": 1,
            "curriculum_id": 123,
            "version_id": None,
            "spacy_analysis": SpacyAnalysis(**spacy_data),
            "gemini_analysis": GeminiAnalysis(**gemini_data),
            "action_verbs_count": 5,
            "quantified_results_count": 3,
            "keywords_score": 8.5,
            "overall_score": 7.8,
            "strengths": ["Experiência sólida"],
            "weaknesses": ["Formatação"],
            "suggestions": ["Melhorar layout"],
            "analysis_date": now,
            "processing_time": 2.5
        }
        
        analysis = CurriculumAnalysisResponse(**data)
        assert analysis.id == 1
        assert analysis.curriculum_id == 123
        assert analysis.action_verbs_count == 5
        assert analysis.overall_score == 7.8
        assert analysis.processing_time == 2.5
        assert isinstance(analysis.spacy_analysis, SpacyAnalysis)
        assert isinstance(analysis.gemini_analysis, GeminiAnalysis)


class TestCurriculumUploadResponse:
    """Testa o schema CurriculumUploadResponse."""
    
    def test_curriculum_upload_response_valid(self):
        """Testa criação válida de CurriculumUploadResponse."""
        now = datetime.now()
        curriculum_data = {
            "id": 1,
            "user_id": 123,
            "original_filename": "cv.pdf",
            "file_path": "/uploads/cv.pdf",
            "file_size": 1024,
            "created_at": now
        }
        
        data = {
            "curriculum": CurriculumResponse(**curriculum_data),
            "analysis": None,
            "message": "Upload realizado com sucesso!"
        }
        
        response = CurriculumUploadResponse(**data)
        assert response.message == "Upload realizado com sucesso!"
        assert response.curriculum.id == 1
        assert response.analysis is None
    
    def test_curriculum_upload_response_default_message(self):
        """Testa mensagem padrão."""
        now = datetime.now()
        curriculum_data = {
            "id": 1,
            "user_id": 123,
            "original_filename": "cv.pdf",
            "file_path": "/uploads/cv.pdf",
            "file_size": 1024,
            "created_at": now
        }
        
        data = {"curriculum": CurriculumResponse(**curriculum_data)}
        response = CurriculumUploadResponse(**data)
        assert response.message == "Currículo enviado com sucesso!"


class TestCurriculumListResponse:
    """Testa o schema CurriculumListResponse."""
    
    def test_curriculum_list_response_valid(self):
        """Testa criação válida de CurriculumListResponse."""
        now = datetime.now()
        curriculum_data = {
            "id": 1,
            "user_id": 123,
            "original_filename": "cv.pdf",
            "file_path": "/uploads/cv.pdf",
            "file_size": 1024,
            "created_at": now
        }
        
        data = {
            "curricula": [CurriculumResponse(**curriculum_data)],
            "total": 1,
            "page": 1,
            "per_page": 10
        }
        
        response = CurriculumListResponse(**data)
        assert response.total == 1
        assert response.page == 1
        assert response.per_page == 10
        assert len(response.curricula) == 1


class TestCurriculumWithAnalysisResponse:
    """Testa o schema CurriculumWithAnalysisResponse."""
    
    def test_curriculum_with_analysis_response_valid(self):
        """Testa criação válida de CurriculumWithAnalysisResponse."""
        now = datetime.now()
        curriculum_data = {
            "id": 1,
            "user_id": 123,
            "original_filename": "cv.pdf",
            "file_path": "/uploads/cv.pdf",
            "file_size": 1024,
            "created_at": now
        }
        
        data = {
            "curriculum": CurriculumResponse(**curriculum_data),
            "latest_analysis": None,
            "versions": [],
            "analysis_history": []
        }
        
        response = CurriculumWithAnalysisResponse(**data)
        assert response.curriculum.id == 1
        assert response.latest_analysis is None
        assert response.versions == []
        assert response.analysis_history == []


class TestCurriculumInfo:
    """Testa o schema CurriculumInfo."""
    
    def test_curriculum_info_valid(self):
        """Testa criação válida de CurriculumInfo."""
        now = datetime.now()
        data = {
            "id": 1,
            "user_id": 123,
            "filename": "cv.pdf",
            "file_path": "/uploads/cv.pdf",
            "upload_date": now
        }
        
        info = CurriculumInfo(**data)
        assert info.id == 1
        assert info.user_id == 123
        assert info.filename == "cv.pdf"
        assert info.file_path == "/uploads/cv.pdf"
        assert info.upload_date == now
    
    def test_curriculum_info_optional_upload_date(self):
        """Testa upload_date opcional."""
        data = {
            "id": 1,
            "user_id": 123,
            "filename": "cv.pdf",
            "file_path": "/uploads/cv.pdf"
        }
        
        info = CurriculumInfo(**data)
        assert info.upload_date is None


class TestCurriculumAnalysis:
    """Testa o schema CurriculumAnalysis."""
    
    def test_curriculum_analysis_valid(self):
        """Testa criação válida de CurriculumAnalysis."""
        now = datetime.now()
        info_data = {
            "id": 1,
            "user_id": 123,
            "filename": "cv.pdf",
            "file_path": "/uploads/cv.pdf",
            "upload_date": now
        }
        
        data = {
            "curriculum_info": CurriculumInfo(**info_data),
            "analysis": {
                "action_verbs": ["desenvolveu", "implementou"],
                "quantified_results": ["5 projetos"],
                "overall_score": 8.5
            }
        }
        
        analysis = CurriculumAnalysis(**data)
        assert analysis.curriculum_info.id == 1
        assert analysis.analysis["overall_score"] == 8.5
        assert len(analysis.analysis["action_verbs"]) == 2


class TestSchemaValidation:
    """Testa validações gerais dos schemas."""
    
    def test_required_fields_validation(self):
        """Testa validação de campos obrigatórios."""
        # CurriculumResponse sem campos obrigatórios
        with pytest.raises(ValidationError):
            CurriculumResponse()
        
        # CurriculumVersionResponse sem campos obrigatórios
        with pytest.raises(ValidationError):
            CurriculumVersionResponse()
    
    def test_field_types_validation(self):
        """Testa validação de tipos de campos."""
        now = datetime.now()
        
        # ID deve ser int
        with pytest.raises(ValidationError):
            CurriculumResponse(
                id="not_an_int",
                user_id=123,
                original_filename="cv.pdf",
                file_path="/uploads/cv.pdf",
                file_size=1024,
                created_at=now
            )
        
        # file_size deve ser int
        with pytest.raises(ValidationError):
            CurriculumResponse(
                id=1,
                user_id=123,
                original_filename="cv.pdf",
                file_path="/uploads/cv.pdf",
                file_size="not_an_int",
                created_at=now
            )
    
    def test_nested_schema_validation(self):
        """Testa validação de schemas aninhados."""
        # SpacyAnalysis inválido dentro de CurriculumAnalysisResponse
        invalid_spacy = {"action_verbs": "should_be_list"}
        
        with pytest.raises(ValidationError):
            SpacyAnalysis(**invalid_spacy)
    
    def test_config_from_attributes(self):
        """Testa se Config.from_attributes está configurado."""
        # Verifica se os schemas têm from_attributes = True
        assert CurriculumResponse.model_config.get('from_attributes') is True
        assert CurriculumVersionResponse.model_config.get('from_attributes') is True
        assert CurriculumAnalysisResponse.model_config.get('from_attributes') is True
        assert CurriculumInfo.model_config.get('from_attributes') is True
        # CurriculumAnalysis não tem Config definido
        assert CurriculumAnalysis.model_config == {}


class TestSchemaInheritance:
    """Testa herança entre schemas."""
    
    def test_curriculum_create_inherits_base(self):
        """Testa se CurriculumCreate herda de CurriculumBase."""
        assert issubclass(CurriculumCreate, CurriculumBase)
    
    def test_curriculum_update_inherits_base(self):
        """Testa se CurriculumUpdate herda de CurriculumBase."""
        assert issubclass(CurriculumUpdate, CurriculumBase)
    
    def test_curriculum_response_inherits_base(self):
        """Testa se CurriculumResponse herda de CurriculumBase."""
        assert issubclass(CurriculumResponse, CurriculumBase)


class TestSchemaEdgeCases:
    """Testa casos extremos dos schemas."""
    
    def test_empty_lists_validation(self):
        """Testa validação de listas vazias."""
        # SpacyAnalysis com listas vazias
        data = {
            "action_verbs": [],
            "quantified_results": [],
            "keywords_found": [],
            "text_statistics": {}
        }
        analysis = SpacyAnalysis(**data)
        assert analysis.action_verbs == []
        assert analysis.quantified_results == []
    
    def test_none_values_validation(self):
        """Testa validação de valores None."""
        # CurriculumResponse com campos opcionais None
        now = datetime.now()
        data = {
            "id": 1,
            "user_id": 123,
            "original_filename": "cv.pdf",
            "file_path": "/uploads/cv.pdf",
            "file_size": 1024,
            "created_at": now,
            "updated_at": None,
            "title": None,
            "description": None
        }
        curriculum = CurriculumResponse(**data)
        assert curriculum.updated_at is None
        assert curriculum.title is None
        assert curriculum.description is None
    
    def test_large_values_validation(self):
        """Testa validação de valores grandes."""
        # file_size muito grande
        now = datetime.now()
        data = {
            "id": 1,
            "user_id": 123,
            "original_filename": "cv.pdf",
            "file_path": "/uploads/cv.pdf",
            "file_size": 999999999,
            "created_at": now
        }
        curriculum = CurriculumResponse(**data)
        assert curriculum.file_size == 999999999
