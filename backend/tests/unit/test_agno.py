"""
Testes unitários para o módulo Agno

Este módulo testa o orquestrador Agno e suas funcionalidades.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.agno import AgnoOrchestrator, AnalysisEngine, GeminiClient


class TestGeminiClient:
    """Testa o cliente do Google Gemini."""
    
    @patch('app.agno.gemini_client.genai')
    def test_gemini_client_initialization_with_api_key(self, mock_genai):
        """Testa inicialização com chave da API."""
        # Mock para simular falha na configuração
        mock_genai.configure.side_effect = Exception("API key inválida")
        
        api_key = "test-api-key"
        client = GeminiClient(api_key)
        
        assert client.api_key == api_key
        assert client.is_configured is False  # Deve falhar devido ao mock
    
    def test_gemini_client_initialization_without_api_key(self):
        """Testa inicialização sem chave da API."""
        with patch('app.agno.gemini_client.settings') as mock_settings:
            mock_settings.gemini_api_key = None
            client = GeminiClient()
            
            assert client.api_key is None
            assert client.is_configured is False
    
    @patch('app.agno.gemini_client.genai')
    def test_gemini_client_configured_successfully(self, mock_genai):
        """Testa configuração bem-sucedida."""
        # Mock para simular configuração bem-sucedida
        mock_genai.configure.return_value = None
        
        api_key = "valid-api-key"
        client = GeminiClient(api_key)
        
        assert client.is_configured is True
    
    def test_generate_qualitative_feedback_without_config(self):
        """Testa geração de feedback sem configuração."""
        client = GeminiClient()
        client._configured = False  # Força configuração como False
        
        feedback = client.generate_qualitative_feedback("test text")
        
        assert "não configurado" in feedback.lower()
    
    def test_analyze_curriculum_structure_without_config(self):
        """Testa análise estrutural sem configuração."""
        client = GeminiClient()
        client._configured = False  # Força configuração como False
        
        result = client.analyze_curriculum_structure("test text")
        
        assert "error" in result
        assert "não configurado" in result["error"].lower()
    
    def test_analyze_keywords_match_without_config(self):
        """Testa análise de palavras-chave sem configuração."""
        client = GeminiClient()
        client._configured = False  # Força configuração como False
        
        result = client.analyze_keywords_match("cv text", "job description")
        
        assert "error" in result
        assert "não configurado" in result["error"].lower()
    
    def test_generate_improvement_suggestions_without_config(self):
        """Testa geração de sugestões sem configuração."""
        client = GeminiClient()
        client._configured = False  # Força configuração como False
        
        suggestions = client.generate_improvement_suggestions("cv text", {})
        
        assert "não configurado" in suggestions[0].lower()
    
    def test_parse_gemini_response_valid_json(self):
        """Testa parse de resposta JSON válida."""
        client = GeminiClient()
        valid_json = '{"key": "value"}'
        
        result = client._parse_gemini_response(valid_json)
        
        assert result == {"key": "value"}
    
    def test_parse_gemini_response_with_json_code_blocks(self):
        """Testa parse de resposta com blocos de código JSON."""
        client = GeminiClient()
        json_with_blocks = '```json\n{"key": "value"}\n```'
        
        result = client._parse_gemini_response(json_with_blocks)
        
        assert result == {"key": "value"}
    
    def test_parse_gemini_response_invalid_json(self):
        """Testa parse de resposta JSON inválida."""
        client = GeminiClient()
        invalid_json = '{"key": "value"'
        
        result = client._parse_gemini_response(invalid_json)
        
        assert "error" in result
        assert "Resposta inválida" in result["error"]


class TestAnalysisEngine:
    """Testa o motor de análise."""
    
    def test_analysis_engine_initialization(self):
        """Testa inicialização do motor de análise."""
        with patch('app.agno.analysis_engine.spacy.load') as mock_load:
            mock_load.side_effect = OSError("Model not found")
            
            engine = AnalysisEngine()
            
            assert engine.spacy_available is False
            assert hasattr(engine, 'action_verbs')
            assert hasattr(engine, 'quantification_patterns')
    
    def test_analyze_quantification_empty_text(self):
        """Testa análise de quantificação com texto vazio."""
        engine = AnalysisEngine()
        result = engine.analyze_quantification("")
        
        assert "numeros_encontrados" in result
        assert result["score_quantificacao"] == 0.0
    
    def test_analyze_quantification_with_regex_fallback(self):
        """Testa análise de quantificação com fallback regex."""
        with patch('app.agno.analysis_engine.spacy.load') as mock_load:
            mock_load.side_effect = OSError("Model not found")
            engine = AnalysisEngine()
            
            text = "Desenvolvi 5 projetos e aumentei 25% da produtividade"
            result = engine.analyze_quantification(text)
            
            assert "numeros_encontrados" in result
            assert "percentuais" in result
            assert result["metodo_analise"] == "regex"
    
    def test_analyze_action_verbs_empty_text(self):
        """Testa análise de verbos com texto vazio."""
        engine = AnalysisEngine()
        result = engine.analyze_action_verbs("")
        
        assert "verbos_encontrados" in result
        assert result["score_verbos"] == 0.0
    
    def test_analyze_action_verbs_with_regex_fallback(self):
        """Testa análise de verbos com fallback regex."""
        with patch('app.agno.analysis_engine.spacy.load') as mock_load:
            mock_load.side_effect = OSError("Model not found")
            engine = AnalysisEngine()
            
            text = "Desenvolvi projetos e implementei soluções"
            result = engine.analyze_action_verbs(text)
            
            assert "verbos_acao" in result
            assert result["metodo_analise"] == "regex"
    
    def test_analyze_text_structure_empty_text(self):
        """Testa análise de estrutura com texto vazio."""
        engine = AnalysisEngine()
        result = engine.analyze_text_structure("")
        
        assert "error" in result
        assert "Texto vazio" in result["error"]
    
    def test_analyze_text_structure_with_content(self):
        """Testa análise de estrutura com conteúdo."""
        with patch('app.agno.analysis_engine.spacy.load') as mock_load:
            mock_load.side_effect = OSError("Model not found")
            engine = AnalysisEngine()
            
            text = "Nome: João\nExperiência: 5 anos\nEducação: Graduação"
            result = engine.analyze_text_structure(text)
            
            assert "secoes" in result
            assert "formatacao" in result
            assert "comprimento" in result
            assert "estrutura_geral" in result
    
    def test_calculate_quantification_score(self):
        """Testa cálculo de score de quantificação."""
        engine = AnalysisEngine()
        
        score = engine._calculate_quantification_score(5, 2, 1, 3, 0, 0, 1)
        
        assert score > 0
        assert score <= 1.0
    
    def test_calculate_verbs_score(self):
        """Testa cálculo de score de verbos."""
        engine = AnalysisEngine()
        
        score = engine._calculate_verbs_score(8, 15)
        
        assert score > 0
        assert score <= 1.0
    
    def test_classify_level(self):
        """Testa classificação de níveis."""
        engine = AnalysisEngine()
        
        assert engine._classify_level(95) == "Excelente"
        assert engine._classify_level(75) == "Bom"
        assert engine._classify_level(45) == "Precisa Melhorar"


class TestAgnoOrchestrator:
    """Testa o orquestrador principal do Agno."""
    
    def test_agno_orchestrator_initialization(self):
        """Testa inicialização do orquestrador."""
        with patch('app.agno.orchestrator.AnalysisEngine') as mock_engine_class:
            with patch('app.agno.orchestrator.GeminiClient') as mock_client_class:
                mock_engine = Mock()
                mock_engine.spacy_available = True
                mock_engine_class.return_value = mock_engine
                
                mock_client = Mock()
                mock_client.is_configured = True
                mock_client_class.return_value = mock_client
                
                orchestrator = AgnoOrchestrator("test-key")
                
                assert orchestrator.analysis_engine == mock_engine
                assert orchestrator.gemini_client == mock_client
    
    def test_analyze_curriculum_comprehensive_empty_text(self):
        """Testa análise completa com texto vazio."""
        with patch('app.agno.orchestrator.AnalysisEngine') as mock_engine_class:
            with patch('app.agno.orchestrator.GeminiClient') as mock_client_class:
                mock_engine = Mock()
                mock_engine_class.return_value = mock_engine
                
                mock_client = Mock()
                mock_client_class.return_value = mock_client
                
                orchestrator = AgnoOrchestrator()
                result = orchestrator.analyze_curriculum_comprehensive("")
                
                assert "error" in result
                assert "Texto do currículo está vazio" in result["error"]
    
    def test_analyze_curriculum_comprehensive_with_content(self):
        """Testa análise completa com conteúdo."""
        with patch('app.agno.orchestrator.AnalysisEngine') as mock_engine_class:
            with patch('app.agno.orchestrator.GeminiClient') as mock_client_class:
                # Mock do motor de análise
                mock_engine = Mock()
                mock_engine.analyze_quantification.return_value = {
                    "score_quantificacao": 0.5,
                    "metodo_analise": "regex"
                }
                mock_engine.analyze_action_verbs.return_value = {
                    "score_verbos": 0.6,
                    "metodo_analise": "regex"
                }
                mock_engine.analyze_text_structure.return_value = {
                    "estrutura_geral": {"score_geral": 75.0}
                }
                mock_engine_class.return_value = mock_engine
                
                # Mock do cliente Gemini
                mock_client = Mock()
                mock_client.is_configured = True
                mock_client.analyze_keywords_match.return_value = {
                    "score_correspondencia": 80.0
                }
                mock_client.generate_qualitative_feedback.return_value = "Feedback teste"
                mock_client.analyze_curriculum_structure.return_value = {
                    "estrutura": {"organizacao": 85}
                }
                mock_client.generate_improvement_suggestions.return_value = ["Sugestão 1"]
                mock_client_class.return_value = mock_client
                
                orchestrator = AgnoOrchestrator()
                result = orchestrator.analyze_curriculum_comprehensive(
                    "Texto de teste do currículo",
                    "Descrição da vaga"
                )
                
                assert "analise_estrutural" in result
                assert "analise_texto" in result
                assert "analise_palavras_chave" in result
                assert "feedback_ia" in result
                assert "pontuacoes" in result
                assert "recomendacoes" in result
                assert "metadados" in result
    
    def test_get_analysis_summary(self):
        """Testa obtenção de resumo da análise."""
        with patch('app.agno.orchestrator.AnalysisEngine') as mock_engine_class:
            with patch('app.agno.orchestrator.GeminiClient') as mock_client_class:
                mock_engine = Mock()
                mock_engine.analyze_quantification.return_value = {
                    "score_quantificacao": 0.5,
                    "numeros_encontrados": ["5", "10"]
                }
                mock_engine.analyze_action_verbs.return_value = {
                    "score_verbos": 0.6,
                    "verbos_acao": ["desenvolvi", "implementei"]
                }
                mock_engine_class.return_value = mock_engine
                
                mock_client = Mock()
                mock_client_class.return_value = mock_client
                
                orchestrator = AgnoOrchestrator()
                result = orchestrator.get_analysis_summary("Texto de teste")
                
                assert "score_rapido" in result
                assert "nivel" in result
                assert "quantificacao" in result
                assert "verbos_acao" in result
    
    def test_health_check(self):
        """Testa verificação de saúde do sistema."""
        with patch('app.agno.orchestrator.AnalysisEngine') as mock_engine_class:
            with patch('app.agno.orchestrator.GeminiClient') as mock_client_class:
                mock_engine = Mock()
                mock_engine.spacy_available = True
                mock_engine.nlp = Mock()
                mock_engine_class.return_value = mock_engine
                
                mock_client = Mock()
                mock_client.is_configured = True
                mock_client.api_key = "test-key"
                mock_client_class.return_value = mock_client
                
                orchestrator = AgnoOrchestrator()
                result = orchestrator.health_check()
                
                assert result["status"] == "operacional"
                assert "ferramentas" in result
                assert result["ferramentas"]["spacy"]["disponivel"] is True
                assert result["ferramentas"]["gemini"]["disponivel"] is True
    
    def test_error_handling_in_comprehensive_analysis(self):
        """Testa tratamento de erros na análise completa."""
        with patch('app.agno.orchestrator.AnalysisEngine') as mock_engine_class:
            with patch('app.agno.orchestrator.GeminiClient') as mock_client_class:
                mock_engine = Mock()
                mock_engine.analyze_quantification.side_effect = Exception("Erro teste")
                mock_engine_class.return_value = mock_engine
                
                mock_client = Mock()
                mock_client_class.return_value = mock_client
                
                orchestrator = AgnoOrchestrator()
                result = orchestrator.analyze_curriculum_comprehensive("Texto teste")
                
                # Verifica se o erro foi capturado na análise estrutural
                assert "analise_estrutural" in result
                assert "quantificacao" in result["analise_estrutural"]
                assert "error" in result["analise_estrutural"]["quantificacao"]
                assert "Erro teste" in result["analise_estrutural"]["quantificacao"]["error"]
                
                # Verifica se a estrutura completa está presente
                assert "analise_texto" in result
                assert "analise_palavras_chave" in result
                assert "feedback_ia" in result
                assert "pontuacoes" in result
                assert "recomendacoes" in result
                assert "resumo" in result
                assert "metadados" in result


class TestAgnoIntegration:
    """Testa integração entre componentes do Agno."""
    
    def test_agno_module_imports(self):
        """Testa se todos os componentes do Agno podem ser importados."""
        try:
            from app.agno import AgnoOrchestrator, AnalysisEngine, GeminiClient
            assert True
        except ImportError as e:
            pytest.fail(f"Falha ao importar módulo Agno: {e}")
    
    def test_agno_analysis_functions_import(self):
        """Testa se as funções de análise do Agno podem ser importadas."""
        try:
            from app.agno import (
                analisar_curriculo_com_agno,
                obter_resumo_agno,
                verificar_saude_agno
            )
            assert True
        except ImportError as e:
            pytest.fail(f"Falha ao importar funções do Agno: {e}")
    
    def test_agno_orchestrator_methods(self):
        """Testa se o orquestrador tem todos os métodos necessários."""
        orchestrator_methods = [
            'analyze_curriculum_comprehensive',
            'get_analysis_summary',
            'health_check'
        ]
        
        for method in orchestrator_methods:
            assert hasattr(AgnoOrchestrator, method), f"Método {method} não encontrado"
    
    def test_analysis_engine_methods(self):
        """Testa se o motor de análise tem todos os métodos necessários."""
        engine_methods = [
            'analyze_quantification',
            'analyze_action_verbs',
            'analyze_text_structure'
        ]
        
        for method in engine_methods:
            assert hasattr(AnalysisEngine, method), f"Método {method} não encontrado"
    
    def test_gemini_client_methods(self):
        """Testa se o cliente Gemini tem todos os métodos necessários."""
        client_methods = [
            'analyze_curriculum_structure',
            'generate_qualitative_feedback',
            'analyze_keywords_match',
            'generate_improvement_suggestions'
        ]
        
        for method in client_methods:
            assert hasattr(GeminiClient, method), f"Método {method} não encontrado"
