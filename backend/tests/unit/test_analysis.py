"""
Testes unitários para o módulo de análise de currículos.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.analysis import (
    analisar_quantificacao,
    analisar_verbos_de_acao,
    calcular_pontuacoes,
    analisar_palavras_chave,
    analisar_curriculo_completo,
    _analisar_quantificacao_mock,
    _analisar_verbos_de_acao_mock,
    _classificar_nivel,
    _gerar_recomendacoes
)


class TestAnalisarQuantificacao:
    """Testes para a função analisar_quantificacao."""
    
    def test_analisar_quantificacao_com_spacy_disponivel(self):
        """Testa análise de quantificação com spaCy disponível."""
        texto_cv = "Desenvolvi 5 projetos, aumentei 25% da performance e gerenciei R$ 100.000 em orçamento."
        
        # Mock do spaCy
        mock_token1 = Mock()
        mock_token1.like_num = True
        mock_token1.text = "5"
        
        mock_token2 = Mock()
        mock_token2.like_num = False
        mock_token2.text = "projetos"
        
        mock_token3 = Mock()
        mock_token3.like_num = True
        mock_token3.text = "25%"
        
        mock_token4 = Mock()
        mock_token4.like_num = False
        mock_token4.text = "R$"
        
        mock_token5 = Mock()
        mock_token5.like_num = True
        mock_token5.text = "100.000"
        
        mock_doc = Mock()
        mock_doc.__iter__ = lambda self: iter([mock_token1, mock_token2, mock_token3, mock_token4, mock_token5])
        
        with patch('app.analysis.SPACY_AVAILABLE', True), \
             patch('app.analysis.nlp') as mock_nlp:
            
            mock_nlp.return_value = mock_doc
            
            resultado = analisar_quantificacao(texto_cv)
            
            assert "numeros_encontrados" in resultado
            assert "percentuais" in resultado
            assert "valores_monetarios" in resultado
            assert "score_quantificacao" in resultado
            assert resultado["score_quantificacao"] > 0
    
    def test_analisar_quantificacao_sem_spacy(self):
        """Testa análise de quantificação sem spaCy disponível."""
        texto_cv = "Desenvolvi 5 projetos e aumentei 25% da performance."
        
        with patch('app.analysis.SPACY_AVAILABLE', False):
            resultado = analisar_quantificacao(texto_cv)
            
            assert "numeros_encontrados" in resultado
            assert "percentuais" in resultado
            assert "score_quantificacao" in resultado
            assert resultado["score_quantificacao"] > 0
    
    def test_analisar_quantificacao_texto_vazio(self):
        """Testa análise de quantificação com texto vazio."""
        with patch('app.analysis.SPACY_AVAILABLE', False):
            resultado = analisar_quantificacao("")
            
            assert resultado["numeros_encontrados"] == []
            assert resultado["score_quantificacao"] == 0.0
    
    def test_analisar_quantificacao_erro_spacy(self):
        """Testa análise de quantificação com erro no spaCy."""
        texto_cv = "Texto com números 123"
        
        with patch('app.analysis.SPACY_AVAILABLE', True), \
             patch('app.analysis.nlp', side_effect=Exception("Erro spaCy")):
            
            resultado = analisar_quantificacao(texto_cv)
            
            # Deve retornar o mock em caso de erro
            assert "numeros_encontrados" in resultado
            assert "score_quantificacao" in resultado


class TestAnalisarVerbosDeAcao:
    """Testes para a função analisar_verbos_de_acao."""
    
    def test_analisar_verbos_com_spacy_disponivel(self):
        """Testa análise de verbos com spaCy disponível."""
        texto_cv = "Desenvolvi sistemas, implementei soluções e gerenciei equipes."
        
        # Mock dos tokens do spaCy
        mock_token1 = Mock()
        mock_token1.pos_ = "VERB"
        mock_token1.lemma_ = "desenvolver"
        
        mock_token2 = Mock()
        mock_token2.pos_ = "NOUN"
        mock_token2.lemma_ = "sistema"
        
        mock_token3 = Mock()
        mock_token3.pos_ = "VERB"
        mock_token3.lemma_ = "implementar"
        
        mock_doc = Mock()
        mock_doc.__iter__ = lambda self: iter([mock_token1, mock_token2, mock_token3])
        
        with patch('app.analysis.SPACY_AVAILABLE', True), \
             patch('app.analysis.nlp') as mock_nlp:
            
            mock_nlp.return_value = mock_doc
            
            resultado = analisar_verbos_de_acao(texto_cv)
            
            assert "verbos_encontrados" in resultado
            assert "verbos_acao" in resultado
            assert "score_verbos" in resultado
            assert resultado["score_verbos"] > 0
    
    def test_analisar_verbos_sem_spacy(self):
        """Testa análise de verbos sem spaCy disponível."""
        texto_cv = "Desenvolvi sistemas e implementei soluções."
        
        with patch('app.analysis.SPACY_AVAILABLE', False):
            resultado = analisar_verbos_de_acao(texto_cv)
            
            assert "verbos_encontrados" in resultado
            assert "verbos_acao" in resultado
            assert "score_verbos" in resultado
            assert resultado["score_verbos"] > 0
    
    def test_analisar_verbos_texto_vazio(self):
        """Testa análise de verbos com texto vazio."""
        with patch('app.analysis.SPACY_AVAILABLE', False):
            resultado = analisar_verbos_de_acao("")
            
            assert resultado["verbos_encontrados"] == []
            assert resultado["verbos_acao"] == []
            assert resultado["score_verbos"] == 0.0
    
    def test_analisar_verbos_erro_spacy(self):
        """Testa análise de verbos com erro no spaCy."""
        texto_cv = "Texto com verbos"
        
        with patch('app.analysis.SPACY_AVAILABLE', True), \
             patch('app.analysis.nlp', side_effect=Exception("Erro spaCy")):
            
            resultado = analisar_verbos_de_acao(texto_cv)
            
            # Deve retornar o mock em caso de erro
            assert "verbos_encontrados" in resultado
            assert "score_verbos" in resultado


class TestCalcularPontuacoes:
    """Testes para a função calcular_pontuacoes."""
    
    def test_calcular_pontuacoes_basicas(self):
        """Testa cálculo básico de pontuações."""
        analise_quant = {"score_quantificacao": 0.5}
        analise_verbos = {"score_verbos": 0.8}
        
        resultado = calcular_pontuacoes(analise_quant, analise_verbos)
        
        assert resultado["pontuacao_quantificacao"] == 50.0
        assert resultado["pontuacao_verbos_acao"] == 80.0
        assert resultado["pontuacao_geral"] == 62.0  # (50 * 0.6) + (80 * 0.4)
        assert "nivel" in resultado
        assert "recomendacoes" in resultado
    
    def test_calcular_pontuacoes_maximas(self):
        """Testa cálculo com pontuações máximas."""
        analise_quant = {"score_quantificacao": 1.0}
        analise_verbos = {"score_verbos": 1.0}
        
        resultado = calcular_pontuacoes(analise_quant, analise_verbos)
        
        assert resultado["pontuacao_quantificacao"] == 100.0
        assert resultado["pontuacao_verbos_acao"] == 100.0
        assert resultado["pontuacao_geral"] == 100.0
    
    def test_calcular_pontuacoes_minimas(self):
        """Testa cálculo com pontuações mínimas."""
        analise_quant = {"score_quantificacao": 0.0}
        analise_verbos = {"score_verbos": 0.0}
        
        resultado = calcular_pontuacoes(analise_quant, analise_verbos)
        
        assert resultado["pontuacao_quantificacao"] == 0.0
        assert resultado["pontuacao_verbos_acao"] == 0.0
        assert resultado["pontuacao_geral"] == 0.0
    
    def test_calcular_pontuacoes_valores_faltando(self):
        """Testa cálculo com valores faltando nas análises."""
        analise_quant = {}
        analise_verbos = {}
        
        resultado = calcular_pontuacoes(analise_quant, analise_verbos)
        
        assert resultado["pontuacao_quantificacao"] == 0.0
        assert resultado["pontuacao_verbos_acao"] == 0.0
        assert resultado["pontuacao_geral"] == 0.0


class TestAnalisarPalavrasChave:
    """Testes para a função analisar_palavras_chave."""
    
    def test_analisar_palavras_chave_basico(self):
        """Testa análise básica de palavras-chave."""
        texto_cv = "Desenvolvedor Python com experiência em Django e PostgreSQL"
        descricao_vaga = "Buscamos desenvolvedor Python, Django, PostgreSQL e AWS"
        
        resultado = analisar_palavras_chave(texto_cv, descricao_vaga)
        
        assert "palavras_chave_encontradas" in resultado
        assert "score_palavras_chave" in resultado
        assert "palavras_faltantes" in resultado
        assert len(resultado["palavras_chave_encontradas"]) > 0
    
    def test_analisar_palavras_chave_texto_vazio(self):
        """Testa análise com texto vazio."""
        resultado = analisar_palavras_chave("", "descrição")
        
        assert resultado["palavras_chave_encontradas"] == []
        assert resultado["score_palavras_chave"] == 0.0
        assert resultado["palavras_faltantes"] == []
    
    def test_analisar_palavras_chave_descricao_vazia(self):
        """Testa análise com descrição da vaga vazia."""
        resultado = analisar_palavras_chave("texto do cv", "")
        
        assert resultado["palavras_chave_encontradas"] == []
        assert resultado["score_palavras_chave"] == 0.0
        assert resultado["palavras_faltantes"] == []
    
    def test_analisar_palavras_chave_case_insensitive(self):
        """Testa análise case-insensitive de palavras-chave."""
        texto_cv = "Desenvolvedor PYTHON com experiência em DJANGO"
        descricao_vaga = "python django postgresql"
        
        resultado = analisar_palavras_chave(texto_cv, descricao_vaga)
        
        assert "python" in [kw.lower() for kw in resultado["palavras_chave_encontradas"]]
        assert "django" in [kw.lower() for kw in resultado["palavras_chave_encontradas"]]


class TestAnalisarCurriculoCompleto:
    """Testes para a função analisar_curriculo_completo."""
    
    def test_analisar_curriculo_completo_basico(self):
        """Testa análise completa de currículo."""
        texto_cv = "Desenvolvedor Python com 5 anos de experiência. Desenvolvi 10 projetos."
        descricao_vaga = "Desenvolvedor Python com experiência em Django"
        
        with patch('app.analysis.SPACY_AVAILABLE', False):
            resultado = analisar_curriculo_completo(texto_cv, descricao_vaga)
            
            assert "quantificacao" in resultado
            assert "verbos_de_acao" in resultado
            assert "pontuacoes" in resultado
            assert "palavras_chave" in resultado
            assert "feedback_qualitativo" in resultado
    
    def test_analisar_curriculo_completo_sem_descricao_vaga(self):
        """Testa análise completa sem descrição da vaga."""
        texto_cv = "Desenvolvedor Python com 5 anos de experiência."
        
        with patch('app.analysis.SPACY_AVAILABLE', False):
            resultado = analisar_curriculo_completo(texto_cv)
            
            assert "quantificacao" in resultado
            assert "verbos_de_acao" in resultado
            assert "pontuacoes" in resultado
            assert "palavras_chave" not in resultado
            assert "feedback_qualitativo" in resultado


class TestFuncoesAuxiliares:
    """Testes para funções auxiliares."""
    
    def test_classificar_nivel(self):
        """Testa classificação de nível baseada na pontuação."""
        assert _classificar_nivel(95.0) == "Excelente"
        assert _classificar_nivel(85.0) == "Muito Bom"
        assert _classificar_nivel(75.0) == "Bom"
        assert _classificar_nivel(65.0) == "Regular"
        assert _classificar_nivel(55.0) == "Abaixo da Média"
        assert _classificar_nivel(45.0) == "Precisa Melhorar"
    
    def test_gerar_recomendacoes(self):
        """Testa geração de recomendações baseadas nas pontuações."""
        pontuacoes = {
            "pontuacao_quantificacao": 50.0,
            "pontuacao_verbos_acao": 80.0,
            "pontuacao_geral": 62.0
        }
        
        recomendacoes = _gerar_recomendacoes(pontuacoes)
        
        assert isinstance(recomendacoes, list)
        assert len(recomendacoes) > 0
        assert all(isinstance(rec, str) for rec in recomendacoes)
    
    def test_gerar_recomendacoes_pontuacoes_altas(self):
        """Testa geração de recomendações com pontuações altas."""
        pontuacoes = {
            "pontuacao_quantificacao": 90.0,
            "pontuacao_verbos_acao": 95.0,
            "pontuacao_geral": 92.0
        }
        
        recomendacoes = _gerar_recomendacoes(pontuacoes)
        
        assert isinstance(recomendacoes, list)
        assert len(recomendacoes) > 0
    
    def test_gerar_recomendacoes_pontuacoes_baixas(self):
        """Testa geração de recomendações com pontuações baixas."""
        pontuacoes = {
            "pontuacao_quantificacao": 20.0,
            "pontuacao_verbos_acao": 30.0,
            "pontuacao_geral": 24.0
        }
        
        recomendacoes = _gerar_recomendacoes(pontuacoes)
        
        assert isinstance(recomendacoes, list)
        assert len(recomendacoes) > 0


class TestFuncoesMock:
    """Testes para as funções mock."""
    
    def test_analisar_quantificacao_mock(self):
        """Testa a função mock de análise de quantificação."""
        texto_cv = "Desenvolvi 5 projetos e aumentei 25% da performance"
        
        resultado = _analisar_quantificacao_mock(texto_cv)
        
        assert "numeros_encontrados" in resultado
        assert "percentuais" in resultado
        assert "valores_monetarios" in resultado
        assert "quantidades" in resultado
        assert "score_quantificacao" in resultado
        assert resultado["score_quantificacao"] > 0
    
    def test_analisar_verbos_de_acao_mock(self):
        """Testa a função mock de análise de verbos."""
        texto_cv = "Desenvolvi sistemas e implementei soluções"
        
        resultado = _analisar_verbos_de_acao_mock(texto_cv)
        
        assert "verbos_encontrados" in resultado
        assert "verbos_acao" in resultado
        assert "score_verbos" in resultado
        assert resultado["score_verbos"] > 0


class TestCasosEdge:
    """Testes para casos extremos e edge cases."""
    
    def test_analisar_quantificacao_texto_muito_longo(self):
        """Testa análise com texto muito longo."""
        texto_cv = "Texto " * 1000 + "com números 123 e 456"
        
        with patch('app.analysis.SPACY_AVAILABLE', False):
            resultado = analisar_quantificacao(texto_cv)
            
            assert "numeros_encontrados" in resultado
            assert resultado["score_quantificacao"] > 0
    
    def test_analisar_verbos_texto_com_caracteres_especiais(self):
        """Testa análise com caracteres especiais."""
        texto_cv = "Desenvolvi sistemas com Python 3.8+ e Django 2.2+"
        
        with patch('app.analysis.SPACY_AVAILABLE', False):
            resultado = analisar_verbos_de_acao(texto_cv)
            
            assert "verbos_encontrados" in resultado
            assert resultado["score_verbos"] > 0
    
    def test_calcular_pontuacoes_valores_extremos(self):
        """Testa cálculo com valores extremos."""
        analise_quant = {"score_quantificacao": 0.0001}
        analise_verbos = {"score_verbos": 0.9999}
        
        resultado = calcular_pontuacoes(analise_quant, analise_verbos)
        
        assert resultado["pontuacao_quantificacao"] == 0.0
        assert resultado["pontuacao_verbos_acao"] == 100.0
        assert resultado["pontuacao_geral"] > 0
    
    def test_analisar_palavras_chave_texto_com_acentos(self):
        """Testa análise com texto contendo acentos."""
        texto_cv = "Desenvolvedor com experiência em programação e análise"
        descricao_vaga = "programação análise desenvolvimento"
        
        resultado = analisar_palavras_chave(texto_cv, descricao_vaga)
        
        assert "palavras_chave_encontradas" in resultado
        assert resultado["score_palavras_chave"] > 0
