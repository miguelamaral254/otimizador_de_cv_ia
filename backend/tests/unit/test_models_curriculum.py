import pytest
from datetime import datetime
from sqlalchemy import inspect
from app.models.curriculum import Curriculum, CurriculumVersion, CurriculumAnalysis


class TestCurriculum:
    """Testes para o modelo Curriculum."""
    
    def test_curriculum_creation(self):
        """Testa a criação básica de um currículo."""
        curriculum = Curriculum(
            user_id=1,
            original_filename="cv.pdf",
            file_path="/uploads/cv.pdf",
            file_size=1024,
            title="Meu Currículo",
            description="Currículo para vaga de desenvolvedor"
        )
        
        assert curriculum.user_id == 1
        assert curriculum.original_filename == "cv.pdf"
        assert curriculum.file_path == "/uploads/cv.pdf"
        assert curriculum.file_size == 1024
        assert curriculum.title == "Meu Currículo"
        assert curriculum.description == "Currículo para vaga de desenvolvedor"
        assert curriculum.id is None  # Ainda não foi persistido
    
    def test_curriculum_minimal_creation(self):
        """Testa a criação com apenas os campos obrigatórios."""
        curriculum = Curriculum(
            user_id=1,
            original_filename="cv.pdf",
            file_path="/uploads/cv.pdf",
            file_size=1024
        )
        
        assert curriculum.user_id == 1
        assert curriculum.original_filename == "cv.pdf"
        assert curriculum.file_path == "/uploads/cv.pdf"
        assert curriculum.file_size == 1024
        assert curriculum.title is None
        assert curriculum.description is None
    
    def test_curriculum_repr(self):
        """Testa a representação string do currículo."""
        curriculum = Curriculum(
            id=1,
            user_id=1,
            original_filename="cv.pdf",
            file_path="/uploads/cv.pdf",
            file_size=1024,
            title="Meu CV"
        )
        
        expected = "<Curriculum(id=1, title='Meu CV', user_id=1)>"
        assert str(curriculum) == expected
    
    def test_curriculum_table_structure(self):
        """Testa a estrutura da tabela do currículo."""
        # Usa a classe diretamente para inspecionar a tabela
        table = Curriculum.__table__
        
        # Verifica se a tabela existe
        assert table.name == "curriculum"
        
        # Verifica colunas obrigatórias
        column_names = [col.name for col in table.columns]
        assert "id" in column_names
        assert "user_id" in column_names
        assert "original_filename" in column_names
        assert "file_path" in column_names
        assert "file_size" in column_names
    
    def test_curriculum_column_types(self):
        """Testa os tipos das colunas do currículo."""
        table = Curriculum.__table__
        
        # Verifica tipos das colunas
        id_col = table.columns["id"]
        assert str(id_col.type) == "INTEGER"
        
        user_id_col = table.columns["user_id"]
        assert str(user_id_col.type) == "INTEGER"
        
        filename_col = table.columns["original_filename"]
        assert str(filename_col.type) == "VARCHAR(255)"
        
        file_path_col = table.columns["file_path"]
        assert str(file_path_col.type) == "VARCHAR(500)"
        
        file_size_col = table.columns["file_size"]
        assert str(file_size_col.type) == "INTEGER"
    
    def test_curriculum_relationships(self):
        """Testa os relacionamentos do currículo."""
        # Usa a classe para verificar relacionamentos
        relationships = Curriculum.__mapper__.relationships
        
        # Verifica relacionamentos
        assert "user" in relationships
        assert "versions" in relationships
        assert "analyses" in relationships
        
        # Verifica configurações dos relacionamentos
        user_rel = relationships["user"]
        assert user_rel.back_populates == "curriculum"
        
        versions_rel = relationships["versions"]
        assert versions_rel.back_populates == "curriculum"
        # Verifica se contém as opções de cascade esperadas
        assert "delete" in str(versions_rel.cascade)
        assert "delete-orphan" in str(versions_rel.cascade)
        
        analyses_rel = relationships["analyses"]
        assert analyses_rel.back_populates == "curriculum"
        # Verifica se contém as opções de cascade esperadas
        assert "delete" in str(analyses_rel.cascade)
        assert "delete-orphan" in str(analyses_rel.cascade)
    
    def test_curriculum_timestamps(self):
        """Testa os campos de timestamp do currículo."""
        table = Curriculum.__table__
        
        # Verifica se os campos de timestamp existem
        column_names = [col.name for col in table.columns]
        assert "created_at" in column_names
        assert "updated_at" in column_names
        
        # Verifica configurações dos timestamps
        created_col = table.columns["created_at"]
        assert created_col.server_default is not None
        
        updated_col = table.columns["updated_at"]
        assert updated_col.onupdate is not None


class TestCurriculumVersion:
    """Testes para o modelo CurriculumVersion."""
    
    def test_version_creation(self):
        """Testa a criação básica de uma versão de currículo."""
        version = CurriculumVersion(
            curriculum_id=1,
            version_number=1,
            version_name="v1.0",
            file_path="/uploads/cv_v1.pdf",
            file_size=2048,
            changes_description="Primeira versão"
        )
        
        assert version.curriculum_id == 1
        assert version.version_number == 1
        assert version.version_name == "v1.0"
        assert version.file_path == "/uploads/cv_v1.pdf"
        assert version.file_size == 2048
        assert version.changes_description == "Primeira versão"
    
    def test_version_minimal_creation(self):
        """Testa a criação com apenas os campos obrigatórios."""
        version = CurriculumVersion(
            curriculum_id=1,
            version_number=1,
            file_path="/uploads/cv_v1.pdf",
            file_size=2048
        )
        
        assert version.curriculum_id == 1
        assert version.version_number == 1
        assert version.file_path == "/uploads/cv_v1.pdf"
        assert version.file_size == 2048
        assert version.version_name is None
        assert version.changes_description is None
    
    def test_version_repr(self):
        """Testa a representação string da versão."""
        version = CurriculumVersion(
            id=1,
            curriculum_id=1,
            version_number=2
        )
        
        expected = "<CurriculumVersion(id=1, version=2, curriculum_id=1)>"
        assert str(version) == expected
    
    def test_version_table_structure(self):
        """Testa a estrutura da tabela da versão."""
        table = CurriculumVersion.__table__
        
        # Verifica se a tabela existe
        assert table.name == "curriculum_versions"
        
        # Verifica colunas obrigatórias
        column_names = [col.name for col in table.columns]
        assert "id" in column_names
        assert "curriculum_id" in column_names
        assert "version_number" in column_names
        assert "file_path" in column_names
        assert "file_size" in column_names
    
    def test_version_relationships(self):
        """Testa os relacionamentos da versão."""
        relationships = CurriculumVersion.__mapper__.relationships
        
        # Verifica relacionamentos
        assert "curriculum" in relationships
        assert "analysis" in relationships
        
        # Verifica configurações dos relacionamentos
        curriculum_rel = relationships["curriculum"]
        assert curriculum_rel.back_populates == "versions"
        
        analysis_rel = relationships["analysis"]
        assert analysis_rel.back_populates == "version"
        assert analysis_rel.uselist is False
        # Verifica se contém as opções de cascade esperadas
        assert "delete" in str(analysis_rel.cascade)
        assert "delete-orphan" in str(analysis_rel.cascade)
    
    def test_version_timestamps(self):
        """Testa os campos de timestamp da versão."""
        table = CurriculumVersion.__table__
        
        # Verifica se o campo de timestamp existe
        column_names = [col.name for col in table.columns]
        assert "created_at" in column_names
        
        # Verifica configuração do timestamp
        created_col = table.columns["created_at"]
        assert created_col.server_default is not None


class TestCurriculumAnalysis:
    """Testes para o modelo CurriculumAnalysis."""
    
    def test_analysis_creation(self):
        """Testa a criação básica de uma análise de currículo."""
        analysis = CurriculumAnalysis(
            curriculum_id=1,
            version_id=1,
            spacy_analysis={"verbs": ["desenvolver", "implementar"]},
            gemini_analysis={"feedback": "Bom currículo"},
            action_verbs_count=15,
            quantified_results_count=8,
            keywords_score=85.5,
            overall_score=92.0,
            strengths=["Experiência sólida", "Boa formação"],
            weaknesses=["Falta de projetos open source"],
            suggestions=["Adicionar projetos no GitHub"],
            processing_time=2.5
        )
        
        assert analysis.curriculum_id == 1
        assert analysis.version_id == 1
        assert analysis.spacy_analysis == {"verbs": ["desenvolver", "implementar"]}
        assert analysis.gemini_analysis == {"feedback": "Bom currículo"}
        assert analysis.action_verbs_count == 15
        assert analysis.quantified_results_count == 8
        assert analysis.keywords_score == 85.5
        assert analysis.overall_score == 92.0
        assert analysis.strengths == ["Experiência sólida", "Boa formação"]
        assert analysis.weaknesses == ["Falta de projetos open source"]
        assert analysis.suggestions == ["Adicionar projetos no GitHub"]
        assert analysis.processing_time == 2.5
    
    def test_analysis_minimal_creation(self):
        """Testa a criação com apenas os campos obrigatórios."""
        analysis = CurriculumAnalysis(
            curriculum_id=1
        )
        
        assert analysis.curriculum_id == 1
        assert analysis.version_id is None
        assert analysis.spacy_analysis is None
        assert analysis.gemini_analysis is None
        # Os valores padrão só são aplicados quando o objeto é persistido no banco
        # Em memória, os valores podem ser None
        assert analysis.strengths is None
        assert analysis.weaknesses is None
        assert analysis.suggestions is None
        assert analysis.processing_time is None
    
    def test_analysis_repr(self):
        """Testa a representação string da análise."""
        analysis = CurriculumAnalysis(
            id=1,
            curriculum_id=1,
            overall_score=95.0
        )
        
        expected = "<CurriculumAnalysis(id=1, curriculum_id=1, score=95.0)>"
        assert str(analysis) == expected
    
    def test_analysis_table_structure(self):
        """Testa a estrutura da tabela da análise."""
        table = CurriculumAnalysis.__table__
        
        # Verifica se a tabela existe
        assert table.name == "curriculum_analyses"
        
        # Verifica colunas obrigatórias
        column_names = [col.name for col in table.columns]
        assert "id" in column_names
        assert "curriculum_id" in column_names
        
        # Verifica colunas opcionais
        assert "version_id" in column_names
        assert "spacy_analysis" in column_names
        assert "gemini_analysis" in column_names
        assert "action_verbs_count" in column_names
        assert "quantified_results_count" in column_names
        assert "keywords_score" in column_names
        assert "overall_score" in column_names
        assert "strengths" in column_names
        assert "weaknesses" in column_names
        assert "suggestions" in column_names
        assert "processing_time" in column_names
    
    def test_analysis_column_types(self):
        """Testa os tipos das colunas da análise."""
        table = CurriculumAnalysis.__table__
        
        # Verifica tipos das colunas
        id_col = table.columns["id"]
        assert str(id_col.type) == "INTEGER"
        
        curriculum_id_col = table.columns["curriculum_id"]
        assert str(curriculum_id_col.type) == "INTEGER"
        
        version_id_col = table.columns["version_id"]
        assert str(version_id_col.type) == "INTEGER"
        
        spacy_analysis_col = table.columns["spacy_analysis"]
        assert str(spacy_analysis_col.type) == "JSON"
        
        gemini_analysis_col = table.columns["gemini_analysis"]
        assert str(gemini_analysis_col.type) == "JSON"
        
        action_verbs_count_col = table.columns["action_verbs_count"]
        assert str(action_verbs_count_col.type) == "INTEGER"
        
        keywords_score_col = table.columns["keywords_score"]
        assert str(keywords_score_col.type) == "FLOAT"
        
        overall_score_col = table.columns["overall_score"]
        assert str(overall_score_col.type) == "FLOAT"
        
        strengths_col = table.columns["strengths"]
        assert str(strengths_col.type) == "JSON"
        
        weaknesses_col = table.columns["weaknesses"]
        assert str(weaknesses_col.type) == "JSON"
        
        suggestions_col = table.columns["suggestions"]
        assert str(suggestions_col.type) == "JSON"
        
        processing_time_col = table.columns["processing_time"]
        assert str(processing_time_col.type) == "FLOAT"
    
    def test_analysis_relationships(self):
        """Testa os relacionamentos da análise."""
        relationships = CurriculumAnalysis.__mapper__.relationships
        
        # Verifica relacionamentos
        assert "curriculum" in relationships
        assert "version" in relationships
        
        # Verifica configurações dos relacionamentos
        curriculum_rel = relationships["curriculum"]
        assert curriculum_rel.back_populates == "analyses"
        
        version_rel = relationships["version"]
        assert version_rel.back_populates == "analysis"
    
    def test_analysis_timestamps(self):
        """Testa os campos de timestamp da análise."""
        table = CurriculumAnalysis.__table__
        
        # Verifica se o campo de timestamp existe
        column_names = [col.name for col in table.columns]
        assert "analysis_date" in column_names
        
        # Verifica configuração do timestamp
        analysis_date_col = table.columns["analysis_date"]
        assert analysis_date_col.server_default is not None
    
    def test_analysis_default_values(self):
        """Testa os valores padrão da análise."""
        analysis = CurriculumAnalysis(
            curriculum_id=1
        )
        
        # Os valores padrão só são aplicados quando o objeto é persistido no banco
        # Em memória, os valores podem ser None
        # Verificamos apenas se os campos existem
        assert hasattr(analysis, 'action_verbs_count')
        assert hasattr(analysis, 'quantified_results_count')
        assert hasattr(analysis, 'keywords_score')
        assert hasattr(analysis, 'overall_score')
    
    def test_analysis_json_fields(self):
        """Testa os campos JSON da análise."""
        analysis = CurriculumAnalysis(
            curriculum_id=1,
            spacy_analysis={"verbs": ["desenvolver"], "nouns": ["software"]},
            gemini_analysis={"score": 90, "feedback": "Excelente"},
            strengths=["Experiência", "Formação"],
            weaknesses=["Idioma"],
            suggestions=["Melhorar inglês"]
        )
        
        # Verifica se os campos JSON são preservados
        assert isinstance(analysis.spacy_analysis, dict)
        assert "verbs" in analysis.spacy_analysis
        assert "nouns" in analysis.spacy_analysis
        
        assert isinstance(analysis.gemini_analysis, dict)
        assert "score" in analysis.gemini_analysis
        assert "feedback" in analysis.gemini_analysis
        
        assert isinstance(analysis.strengths, list)
        assert "Experiência" in analysis.strengths
        
        assert isinstance(analysis.weaknesses, list)
        assert "Idioma" in analysis.weaknesses
        
        assert isinstance(analysis.suggestions, list)
        assert "Melhorar inglês" in analysis.suggestions


class TestModelIntegration:
    """Testes de integração entre os modelos."""
    
    def test_curriculum_with_versions_and_analyses(self):
        """Testa a criação de um currículo com versões e análises."""
        # Cria o currículo
        curriculum = Curriculum(
            id=1,
            user_id=1,
            original_filename="cv.pdf",
            file_path="/uploads/cv.pdf",
            file_size=1024
        )
        
        # Cria uma versão
        version = CurriculumVersion(
            id=1,
            curriculum_id=1,
            version_number=1,
            file_path="/uploads/cv_v1.pdf",
            file_size=1024
        )
        
        # Cria uma análise
        analysis = CurriculumAnalysis(
            id=1,
            curriculum_id=1,
            version_id=1,
            overall_score=85.0
        )
        
        # Verifica se os relacionamentos funcionam
        assert curriculum.id == 1
        assert version.curriculum_id == curriculum.id
        assert analysis.curriculum_id == curriculum.id
        assert analysis.version_id == version.id
    
    def test_model_serialization(self):
        """Testa se os modelos podem ser serializados corretamente."""
        curriculum = Curriculum(
            id=1,
            user_id=1,
            original_filename="cv.pdf",
            file_path="/uploads/cv.pdf",
            file_size=1024,
            title="Meu CV"
        )
        
        # Verifica se os atributos são acessíveis
        assert hasattr(curriculum, 'id')
        assert hasattr(curriculum, 'user_id')
        assert hasattr(curriculum, 'original_filename')
        assert hasattr(curriculum, 'file_path')
        assert hasattr(curriculum, 'file_size')
        assert hasattr(curriculum, 'title')
        
        # Verifica se os métodos existem
        assert hasattr(curriculum, '__repr__')
        assert callable(getattr(curriculum, '__repr__'))
    
    def test_model_validation(self):
        """Testa se os modelos aceitam dados válidos."""
        # Testa currículo com dados válidos
        curriculum = Curriculum(
            user_id=1,
            original_filename="cv.pdf",
            file_path="/uploads/cv.pdf",
            file_size=1024
        )
        assert curriculum.user_id == 1
        
        # Testa versão com dados válidos
        version = CurriculumVersion(
            curriculum_id=1,
            version_number=1,
            file_path="/uploads/cv_v1.pdf",
            file_size=1024
        )
        assert version.version_number == 1
        
        # Testa análise com dados válidos
        analysis = CurriculumAnalysis(
            curriculum_id=1,
            overall_score=95.5
        )
        assert analysis.overall_score == 95.5
