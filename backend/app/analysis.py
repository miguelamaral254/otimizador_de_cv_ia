"""
Módulo de Análise de Currículos com IA

Este módulo contém todas as funções de análise de currículos usando:
- spaCy para análise estrutural (verbos, quantificação)
- Google Gemini para feedback qualitativo
- Análise de palavras-chave e métricas
- Agno para orquestração inteligente das análises
"""

import re
import os
from typing import Dict, List, Tuple, Any
import spacy
import google.generativeai as genai
from app.core.config import settings
from app.agno import AgnoOrchestrator

# --- Configuração Inicial ---
try:
    nlp = spacy.load(settings.spacy_model)
    SPACY_AVAILABLE = True
except OSError:
    print(f"Modelo spaCy não encontrado. Execute 'python -m spacy download {settings.spacy_model}'")
    print("Usando modelo mock para desenvolvimento e testes...")
    nlp = None
    SPACY_AVAILABLE = False

# Configura a API do Gemini com a chave das configurações
gemini_api_key = settings.gemini_api_key
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

# Instância global do orquestrador Agno
agno_orchestrator = AgnoOrchestrator(gemini_api_key)

# --- Funções de Análise com spaCy ---

def analisar_quantificacao(texto_cv: str) -> Dict[str, Any]:
    """
    Analisa a quantificação no currículo usando spaCy.
    
    Args:
        texto_cv: Texto do currículo
        
    Returns:
        Dicionário com análise de quantificação
    """
    if not texto_cv:
        return {
            "numeros_encontrados": [],
            "percentuais": [],
            "valores_monetarios": [],
            "quantidades": [],
            "score_quantificacao": 0.0
        }
    
    if not SPACY_AVAILABLE:
        # Modelo mock para desenvolvimento e testes
        return _analisar_quantificacao_mock(texto_cv)
    
    try:
        doc = nlp(texto_cv)
        
        # Extrai números e quantificações
        numeros = []
        percentuais = []
        valores_monetarios = []
        quantidades = []
        
        for token in doc:
            # Números simples
            if token.like_num:
                numeros.append(token.text)
            
            # Percentuais
            if "%" in token.text:
                percentuais.append(token.text)
            
            # Valores monetários (R$, $, €)
            if any(symbol in token.text for symbol in ["R$", "$", "€", "USD", "EUR"]):
                valores_monetarios.append(token.text)
            
            # Quantidades com unidades
            if token.like_num and token.nbor().is_alpha:
                quantidades.append(f"{token.text} {token.nbor().text}")
        
        # Calcula score baseado na quantidade de números encontrados
        score = min(len(numeros) * 0.2, 1.0)
        
        return {
            "numeros_encontrados": numeros,
            "percentuais": percentuais,
            "valores_monetarios": valores_monetarios,
            "quantidades": quantidades,
            "score_quantificacao": score
        }
        
    except Exception as e:
        print(f"Erro na análise de quantificação: {e}")
        return _analisar_quantificacao_mock(texto_cv)

def _analisar_quantificacao_mock(texto_cv: str) -> Dict[str, Any]:
    """Modelo mock para análise de quantificação quando spaCy não está disponível."""
    # Regex simples para encontrar números
    numeros = re.findall(r'\b\d+(?:\.\d+)?\b', texto_cv)
    percentuais = re.findall(r'\b\d+(?:\.\d+)?%\b', texto_cv)
    valores_monetarios = re.findall(r'R?\$?\s*\d+(?:\.\d+)?', texto_cv)
    
    score = min(len(numeros) * 0.15, 1.0)
    
    return {
        "numeros_encontrados": numeros,
        "percentuais": percentuais,
        "valores_monetarios": valores_monetarios,
        "quantidades": [],
        "score_quantificacao": score
    }

def analisar_verbos_de_acao(texto_cv: str) -> Dict[str, Any]:
    """
    Analisa verbos de ação no currículo usando spaCy.
    
    Args:
        texto_cv: Texto do currículo
        
    Returns:
        Dicionário com análise de verbos de ação
    """
    if not texto_cv:
        return {
            "verbos_encontrados": [],
            "verbos_acao": [],
            "score_verbos": 0.0
        }
    
    if not SPACY_AVAILABLE:
        # Modelo mock para desenvolvimento e testes
        return _analisar_verbos_de_acao_mock(texto_cv)
    
    try:
        doc = nlp(texto_cv)
        
        verbos_acao = []
        verbos_gerais = []
        
        # Lista de verbos de ação comuns em currículos
        verbos_acao_comuns = {
            'desenvolver', 'implementar', 'criar', 'construir', 'liderar', 'gerenciar',
            'otimizar', 'melhorar', 'aumentar', 'reduzir', 'analisar', 'resolver',
            'coordenar', 'supervisionar', 'treinar', 'mentorar', 'planejar', 'executar',
            'monitorar', 'avaliar', 'testar', 'deployar', 'configurar', 'manter'
        }
        
        for token in doc:
            if token.pos_ == "VERB":
                verbos_gerais.append(token.lemma_)
                if token.lemma_.lower() in verbos_acao_comuns:
                    verbos_acao.append(token.lemma_)
        
        # Calcula score baseado na quantidade de verbos de ação
        score = min(len(verbos_acao) * 0.1, 1.0)
        
        return {
            "verbos_encontrados": verbos_gerais,
            "verbos_acao": verbos_acao,
            "score_verbos": score
        }
        
    except Exception as e:
        print(f"Erro na análise de verbos: {e}")
        return _analisar_verbos_de_acao_mock(texto_cv)

def _analisar_verbos_de_acao_mock(texto_cv: str) -> Dict[str, Any]:
    """Modelo mock para análise de verbos quando spaCy não está disponível."""
    # Regex para encontrar verbos comuns
    verbos_comuns = [
        'desenvolvi', 'implementei', 'criei', 'construi', 'liderei', 'gerenciei',
        'otimizei', 'melhorei', 'aumentei', 'reduzi', 'analisei', 'resolvi',
        'coordenei', 'supervisionei', 'treinei', 'mentorei', 'planejei', 'executei',
        'monitorei', 'avaliei', 'testei', 'deployei', 'configurei', 'mantive'
    ]
    
    verbos_encontrados = []
    for verbo in verbos_comuns:
        if verbo in texto_cv.lower():
            verbos_encontrados.append(verbo)
    
    score = min(len(verbos_encontrados) * 0.1, 1.0)
    
    return {
        "verbos_encontrados": verbos_encontrados,
        "verbos_acao": verbos_encontrados,
        "score_verbos": score
    }

def calcular_pontuacoes(
    analise_quant: Dict[str, Any], 
    analise_verbos: Dict[str, Any]
) -> Dict[str, float]:
    """
    Calcula pontuações baseadas nas análises de quantificação e verbos.
    
    Args:
        analise_quant: Resultado da análise de quantificação
        analise_verbos: Resultado da análise de verbos
        
    Returns:
        Dicionário com pontuações calculadas
    """
    # Pontuação de quantificação (0-100)
    pontuacao_quantificacao = analise_quant.get("score_quantificacao", 0.0) * 100
    
    # Pontuação de verbos de ação (0-100)
    pontuacao_verbos_acao = analise_verbos.get("score_verbos", 0.0) * 100
    
    # Pontuação geral (média ponderada)
    pontuacao_geral = (pontuacao_quantificacao * 0.6) + (pontuacao_verbos_acao * 0.4)
    
    # Classificação baseada na pontuação
    nivel = _classificar_nivel(pontuacao_geral)
    
    # Recomendações baseadas nas pontuações
    recomendacoes = _gerar_recomendacoes({
        "pontuacao_quantificacao": pontuacao_quantificacao,
        "pontuacao_verbos_acao": pontuacao_verbos_acao,
        "pontuacao_geral": pontuacao_geral
    })
    
    return {
        "pontuacao_quantificacao": round(pontuacao_quantificacao, 1),
        "pontuacao_verbos_acao": round(pontuacao_verbos_acao, 1),
        "pontuacao_geral": round(pontuacao_geral, 1),
        "nivel": nivel,
        "recomendacoes": recomendacoes
    }

def analisar_palavras_chave(texto_cv: str, descricao_vaga: str) -> Dict[str, Any]:
    """
    Analisa palavras-chave do currículo em relação à descrição da vaga.
    
    Args:
        texto_cv: Texto do currículo
        descricao_vaga: Descrição da vaga
        
    Returns:
        Dicionário com análise de palavras-chave
    """
    if not texto_cv or not descricao_vaga:
        return {
            "palavras_chave_encontradas": [],
            "score_palavras_chave": 0.0,
            "palavras_faltantes": []
        }
    
    # Converte para minúsculas para comparação
    texto_lower = texto_cv.lower()
    descricao_lower = descricao_vaga.lower()
    
    # Extrai palavras-chave da descrição da vaga
    palavras_chave_vaga = set(re.findall(r'\b\w{3,}\b', descricao_lower))
    
    # Remove palavras comuns que não são relevantes
    palavras_comuns = {
        'com', 'para', 'que', 'uma', 'por', 'mais', 'como', 'mas', 'foi', 'ele',
        'das', 'tem', 'à', 'seu', 'sua', 'ou', 'ser', 'quando', 'muito', 'nos',
        'já', 'está', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela',
        'entre', 'era', 'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus', 'suas',
        'minha', 'têm', 'na', 'nos', 'ela', 'e', 'também', 'você', 'dessa', 'nela',
        'porque', 'essa', 'num', 'nem', 'suas', 'meu', 'às', 'minha', 'numa', 'pelos',
        'elas', 'havia', 'seja', 'qual', 'nós', 'lhe', 'deles', 'essas', 'esses',
        'pelas', 'este', 'dele', 'tu', 'te', 'vocês', 'vos', 'lhes', 'meus', 'minhas',
        'teu', 'tua', 'teus', 'tuas', 'nosso', 'nossa', 'nossos', 'nossas', 'dela',
        'delas', 'esta', 'estes', 'estas', 'aquele', 'aquela', 'aqueles', 'aquelas',
        'isto', 'aquilo', 'estou', 'está', 'estamos', 'estão', 'estive', 'esteve',
        'estivemos', 'estiveram', 'estava', 'estávamos', 'estavam', 'estivera',
        'estivéramos', 'esteja', 'estejamos', 'estejam', 'estivesse', 'estivéssemos',
        'estivessem', 'estiver', 'estivermos', 'estiverem', 'hei', 'há', 'havemos',
        'hão', 'houve', 'houvemos', 'houveram', 'houvera', 'houvéramos', 'haja',
        'hajamos', 'hajam', 'houvesse', 'houvéssemos', 'houvessem', 'houver',
        'houvermos', 'houverem', 'houverei', 'houverá', 'houveremos', 'houverão',
        'houveria', 'houveríamos', 'houveriam', 'sou', 'somos', 'são', 'era',
        'éramos', 'eram', 'fui', 'foi', 'fomos', 'foram', 'fora', 'fôramos',
        'seja', 'sejamos', 'sejam', 'fosse', 'fôssemos', 'fossem', 'for',
        'formos', 'forem', 'serei', 'será', 'seremos', 'serão', 'seria',
        'seríamos', 'seriam', 'tenho', 'tem', 'temos', 'têm', 'tinha',
        'tínhamos', 'tinham', 'tive', 'teve', 'tivemos', 'tiveram', 'tivera',
        'tivéramos', 'tenha', 'tenhamos', 'tenham', 'tivesse', 'tivéssemos',
        'tivessem', 'tiver', 'tivermos', 'tiverem', 'terei', 'terá', 'teremos',
        'terão', 'teria', 'teríamos', 'teriam'
    }
    
    palavras_chave_vaga = palavras_chave_vaga - palavras_comuns
    
    # Encontra palavras-chave no currículo
    palavras_chave_encontradas = []
    palavras_faltantes = []
    
    for palavra in palavras_chave_vaga:
        if palavra in texto_lower:
            palavras_chave_encontradas.append(palavra)
        else:
            palavras_faltantes.append(palavra)
    
    # Calcula score baseado na quantidade de palavras-chave encontradas
    total_palavras = len(palavras_chave_vaga)
    if total_palavras > 0:
        score = len(palavras_chave_encontradas) / total_palavras
    else:
        score = 0.0
    
    return {
        "palavras_chave_encontradas": palavras_chave_encontradas,
        "palavras_faltantes": palavras_faltantes,
        "score_palavras_chave": round(score * 100, 1),
        "total_palavras_chave": total_palavras
    }

# --- Função de Análise com LLM (Gemini) ---

def gerar_feedback_qualitativo_gemini(texto_cv: str) -> str:
    """
    Gera feedback qualitativo sobre o currículo usando Google Gemini.
    
    Args:
        texto_cv: Texto do currículo
        
    Returns:
        Feedback qualitativo em texto
    """
    if not gemini_api_key or not texto_cv:
        return "A integração com IA generativa não está configurada ou o texto do CV está vazio."
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        Analise o seguinte texto de currículo e forneça um parágrafo de feedback construtivo (em até 100 palavras).
        Foque em pontos fortes e em uma sugestão principal de melhoria geral.
        
        Texto do Currículo:
        ---
        {texto_cv}
        ---
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return "Não foi possível gerar o feedback da IA neste momento."

# --- Função Principal de Análise ---

def analisar_curriculo_completo(texto_cv: str, descricao_vaga: str = None) -> Dict[str, Any]:
    """
    Executa análise completa do currículo.
    
    Args:
        texto_cv: Texto do currículo
        descricao_vaga: Descrição da vaga (opcional)
        
    Returns:
        Dicionário com resultado completo da análise
    """
    if not texto_cv:
        return {
            "erro": "Texto do currículo está vazio",
            "feedback_qualitativo": "",
            "quantificacao": {},
            "verbos_de_acao": {},
            "pontuacoes": {},
            "palavras_chave": {}
        }
    
    # Executa análises estruturais
    analise_quant = analisar_quantificacao(texto_cv)
    analise_verbos = analisar_verbos_de_acao(texto_cv)
    pontuacoes = calcular_pontuacoes(analise_quant, analise_verbos)
    
    # Executa análise qualitativa
    feedback_gemini = gerar_feedback_qualitativo_gemini(texto_cv)
    
    # Compila resultado final
    resultado = {
        "feedback_qualitativo": feedback_gemini,
        "quantificacao": analise_quant,
        "verbos_de_acao": analise_verbos,
        "pontuacoes": pontuacoes,
        "spacy_disponivel": SPACY_AVAILABLE
    }
    
    # Adiciona análise de palavras-chave se descrição da vaga for fornecida
    if descricao_vaga:
        resultado["palavras_chave"] = analisar_palavras_chave(texto_cv, descricao_vaga)
    
    return resultado

def analisar_curriculo_com_agno(texto_cv: str, descricao_vaga: str = None) -> Dict[str, Any]:
    """
    Executa análise completa do currículo usando o orquestrador Agno.
    
    Args:
        texto_cv: Texto do currículo
        descricao_vaga: Descrição da vaga (opcional)
        
    Returns:
        Análise completa orquestrada pelo Agno
    """
    try:
        return agno_orchestrator.analyze_curriculum_comprehensive(
            cv_text=texto_cv,
            job_description=descricao_vaga,
            include_ai_feedback=True,
            include_structure_analysis=True
        )
    except Exception as e:
        print(f"Erro na análise com Agno: {e}")
        # Fallback para análise tradicional
        return analisar_curriculo_completo(texto_cv, descricao_vaga)

def obter_resumo_agno(texto_cv: str) -> Dict[str, Any]:
    """
    Obtém resumo rápido da análise usando Agno.
    
    Args:
        texto_cv: Texto do currículo
        
    Returns:
        Resumo da análise
    """
    try:
        return agno_orchestrator.get_analysis_summary(texto_cv)
    except Exception as e:
        print(f"Erro no resumo Agno: {e}")
        return {"error": str(e)}

def verificar_saude_agno() -> Dict[str, Any]:
    """
    Verifica a saúde de todas as ferramentas de análise.
    
    Returns:
        Status das ferramentas
    """
    try:
        return agno_orchestrator.health_check()
    except Exception as e:
        print(f"Erro no health check: {e}")
        return {"error": str(e)}

# --- Funções Auxiliares ---

def _classificar_nivel(score: float) -> str:
    """Classifica o nível do currículo baseado na pontuação."""
    if score >= 90:
        return "Excelente"
    elif score >= 80:
        return "Muito Bom"
    elif score >= 70:
        return "Bom"
    elif score >= 60:
        return "Regular"
    elif score >= 50:
        return "Abaixo da Média"
    else:
        return "Precisa Melhorar"

def _gerar_recomendacoes(pontuacoes: Dict[str, float]) -> List[str]:
    """Gera recomendações baseadas nas pontuações."""
    recomendacoes = []
    
    if pontuacoes.get("pontuacao_quantificacao", 0) < 60:
        recomendacoes.append("Adicione mais números e métricas quantificáveis ao seu currículo")
    
    if pontuacoes.get("pontuacao_verbos_acao", 0) < 60:
        recomendacoes.append("Use mais verbos de ação para descrever suas realizações")
    
    if pontuacoes.get("pontuacao_geral", 0) < 70:
        recomendacoes.append("Considere revisar a estrutura e conteúdo geral do currículo")
    
    if not recomendacoes:
        recomendacoes.append("Seu currículo está bem estruturado! Continue assim!")
    
    return recomendacoes
