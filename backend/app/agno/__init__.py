"""
Módulo Agno - Orquestrador Inteligente de Análise de Currículos

Este módulo utiliza o Agno para coordenar e otimizar todas as ferramentas
de análise de IA, incluindo spaCy, Google Gemini e análises customizadas.
"""

from .orchestrator import AgnoOrchestrator
from .analysis_engine import AnalysisEngine
from .gemini_client import GeminiClient
from .analysis import (
    analisar_quantificacao,
    analisar_verbos_de_acao,
    calcular_pontuacoes,
    analisar_palavras_chave,
    gerar_feedback_qualitativo_gemini,
    analisar_curriculo_completo,
    analisar_curriculo_com_agno,
    obter_resumo_agno,
    verificar_saude_agno,
    # Funções auxiliares para testes
    _analisar_quantificacao_mock,
    _analisar_verbos_de_acao_mock,
    _classificar_nivel,
    _gerar_recomendacoes
)

__all__ = [
    "AgnoOrchestrator",
    "AnalysisEngine", 
    "GeminiClient",
    # Funções de análise
    "analisar_quantificacao",
    "analisar_verbos_de_acao",
    "calcular_pontuacoes",
    "analisar_palavras_chave",
    "gerar_feedback_qualitativo_gemini",
    "analisar_curriculo_completo",
    "analisar_curriculo_com_agno",
    "obter_resumo_agno",
    "verificar_saude_agno",
    # Funções auxiliares para testes
    "_analisar_quantificacao_mock",
    "_analisar_verbos_de_acao_mock",
    "_classificar_nivel",
    "_gerar_recomendacoes"
]

