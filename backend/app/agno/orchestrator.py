"""
Orquestrador Principal do Agno

Este módulo coordena todas as ferramentas de análise de IA, incluindo
spaCy, Google Gemini e análises customizadas, fornecendo uma interface
unificada para análise de currículos.
"""

import logging
import time
from typing import Dict, Any, Optional, List
from .analysis_engine import AnalysisEngine
from .gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class AgnoOrchestrator:
    """
    Orquestrador principal que coordena todas as ferramentas de análise.
    
    O Agno orquestra:
    - Análise estrutural com spaCy
    - Análise qualitativa com Google Gemini
    - Análise de palavras-chave
    - Geração de recomendações
    - Consolidação de resultados
    """
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        """
        Inicializa o orquestrador Agno.
        
        Args:
            gemini_api_key: Chave da API do Gemini (opcional)
        """
        self.analysis_engine = AnalysisEngine()
        self.gemini_client = GeminiClient(gemini_api_key)
        
        logger.info("Orquestrador Agno inicializado")
        logger.info(f"spaCy disponível: {self.analysis_engine.spacy_available}")
        logger.info(f"Gemini configurado: {self.gemini_client.is_configured}")
    
    async def analyze_curriculum_comprehensive(
        self, 
        cv_text: str, 
        job_description: Optional[str] = None,
        include_ai_feedback: bool = True,
        include_structure_analysis: bool = True
    ) -> Dict[str, Any]:
        """
        Executa análise completa do currículo usando todas as ferramentas disponíveis.
        
        Args:
            cv_text: Texto do currículo
            job_description: Descrição da vaga (opcional)
            include_ai_feedback: Se deve incluir feedback da IA
            include_structure_analysis: Se deve incluir análise estrutural
            
        Returns:
            Análise completa do currículo
        """
        if not cv_text:
            return self._empty_analysis_result()
        
        start_time = time.time()
        logger.info("Iniciando análise completa do currículo")
        
        try:
            # 1. Análises estruturais (spaCy + regex)
            structural_analysis = await self._perform_structural_analysis(cv_text)
            
            # 2. Análise de estrutura do texto
            if include_structure_analysis:
                text_structure = self.analysis_engine.analyze_text_structure(cv_text)
            else:
                text_structure = {}
            
            # 3. Análise de palavras-chave (se descrição da vaga fornecida)
            keyword_analysis = {}
            if job_description:
                keyword_analysis = await self._perform_keyword_analysis(cv_text, job_description)
            
            # 4. Feedback da IA (Gemini)
            ai_feedback = {}
            if include_ai_feedback and self.gemini_client.is_configured:
                ai_feedback = await self._perform_ai_analysis(cv_text, job_description)
            
            # 5. Cálculo de pontuações e classificação
            scores = self._calculate_comprehensive_scores(
                structural_analysis, 
                text_structure, 
                keyword_analysis
            )
            
            # 6. Geração de recomendações
            recommendations = self._generate_recommendations(
                cv_text, 
                structural_analysis, 
                text_structure, 
                keyword_analysis, 
                scores
            )
            
            # 7. Consolidação dos resultados
            final_result = self._consolidate_results(
                structural_analysis,
                text_structure,
                keyword_analysis,
                ai_feedback,
                scores,
                recommendations
            )
            
            execution_time = time.time() - start_time
            final_result["metadados"] = {
                "tempo_execucao": round(execution_time, 2),
                "ferramentas_utilizadas": self._get_used_tools(),
                "timestamp": time.time()
            }
            
            logger.info(f"Análise completa concluída em {execution_time:.2f}s")
            return final_result
            
        except Exception as e:
            logger.error(f"Erro na análise completa: {e}")
            return self._error_analysis_result(str(e))
    
    async def _perform_structural_analysis(self, cv_text: str) -> Dict[str, Any]:
        """Executa análises estruturais usando spaCy e regex."""
        try:
            # Convertendo para métodos síncronos
            quantification = await self._analyze_quantification_sync(cv_text)
            action_verbs = await self._analyze_action_verbs_sync(cv_text)
            
            return {
                "quantificacao": quantification,
                "verbos_de_acao": action_verbs
            }
        except Exception as e:
            logger.error(f"Erro na análise estrutural: {e}")
            return {
                "quantificacao": {"error": str(e)},
                "verbos_de_acao": {"error": str(e)}
            }
    
    async def _analyze_quantification_sync(self, text: str) -> Dict[str, Any]:
        """Versão síncrona da análise de quantificação."""
        try:
            if hasattr(self.analysis_engine, 'analyze_quantification'):
                # Se o método existe, tenta chamá-lo de forma assíncrona
                result = await self.analysis_engine.analyze_quantification(text)
                return result
            else:
                return self._simple_quantification_analysis(text)
        except Exception as e:
            logger.error(f"Erro na análise de quantificação assíncrona: {e}")
            return self._simple_quantification_analysis(text)
    
    async def _analyze_action_verbs_sync(self, text: str) -> Dict[str, Any]:
        """Versão assíncrona da análise de verbos de ação."""
        try:
            if hasattr(self.analysis_engine, 'analyze_action_verbs'):
                # Se o método existe, tenta chamá-lo de forma assíncrona
                result = await self.analysis_engine.analyze_action_verbs(text)
                return result
            else:
                return self._simple_action_verbs_analysis(text)
        except Exception as e:
            logger.error(f"Erro na análise de verbos de ação assíncrona: {e}")
            return self._simple_action_verbs_analysis(text)
    
    def _simple_quantification_analysis(self, text: str) -> Dict[str, Any]:
        """Análise simples de quantificação usando regex."""
        import re
        
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        percentages = re.findall(r'\b\d+(?:\.\d+)?%\b', text)
        currency = re.findall(r'R?\$?\s*\d+(?:,\d{3})*(?:\.\d{2})?', text)
        
        score = min(len(numbers) * 0.1, 1.0)
        
        return {
            "total": len(numbers),
            "items": numbers[:10],  # Limita a 10 itens
            "percentuais": percentages,
            "valores_monetarios": currency,
            "score_quantificacao": round(score, 3)
        }
    
    def _simple_action_verbs_analysis(self, text: str) -> Dict[str, Any]:
        """Análise simples de verbos de ação usando regex."""
        import re
        
        # Verbos de ação comuns em currículos
        action_verbs = [
            'desenvolver', 'implementar', 'criar', 'construir', 'liderar', 'gerenciar',
            'otimizar', 'melhorar', 'aumentar', 'reduzir', 'analisar', 'resolver',
            'coordenar', 'supervisionar', 'treinar', 'mentorar', 'planejar', 'executar'
        ]
        
        text_lower = text.lower()
        found_verbs = [verb for verb in action_verbs if verb in text_lower]
        
        score = min(len(found_verbs) * 0.2, 1.0)
        
        return {
            "total": len(found_verbs),
            "items": found_verbs,
            "score_verbos": round(score, 3)
        }
    
    async def _perform_keyword_analysis(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Executa análise de palavras-chave."""
        try:
            if self.gemini_client.is_configured:
                # Usa Gemini para análise mais inteligente
                return await self.gemini_client.analyze_keywords_match(cv_text, job_description)
            else:
                # Fallback para análise simples
                return self._simple_keyword_analysis(cv_text, job_description)
        except Exception as e:
            logger.error(f"Erro na análise de palavras-chave: {e}")
            return {"error": str(e)}
    
    def _simple_keyword_analysis(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Análise simples de palavras-chave usando regex."""
        import re
        
        cv_lower = cv_text.lower()
        job_lower = job_description.lower()
        
        # Extrai palavras-chave da descrição da vaga
        job_keywords = set(re.findall(r'\b\w{3,}\b', job_lower))
        
        # Remove palavras comuns
        common_words = {
            'com', 'para', 'que', 'uma', 'por', 'mais', 'como', 'mas', 'foi', 'ele',
            'das', 'tem', 'à', 'seu', 'sua', 'ou', 'ser', 'quando', 'muito', 'nos'
        }
        job_keywords = job_keywords - common_words
        
        # Encontra correspondências
        found_keywords = [kw for kw in job_keywords if kw in cv_lower]
        missing_keywords = list(job_keywords - set(found_keywords))
        
        score = len(found_keywords) / max(len(job_keywords), 1)
        
        return {
            "score": round(score, 3),
            "items": found_keywords[:10],  # Limita a 10 itens
            "correspondencia": round(score * 100, 1),
            "palavras_chave_encontradas": found_keywords,
            "palavras_chave_faltantes": missing_keywords,
            "total_palavras_chave": len(job_keywords),
            "metodo_analise": "regex_simples"
        }
    
    async def _perform_ai_analysis(self, cv_text: str, job_description: Optional[str]) -> Dict[str, Any]:
        """Executa análises usando IA (Gemini)."""
        try:
            ai_results = {}
            
            # Feedback qualitativo
            feedback = await self.gemini_client.generate_qualitative_feedback(cv_text, job_description)
            ai_results["feedback_qualitativo"] = feedback
            
            # Análise estrutural com IA
            structure_analysis = await self.gemini_client.analyze_curriculum_structure(cv_text)
            ai_results["analise_estrutural_ia"] = structure_analysis
            
            # Sugestões de melhoria
            if "error" not in structure_analysis:
                suggestions = await self.gemini_client.generate_improvement_suggestions(cv_text, structure_analysis)
                ai_results["sugestoes_melhoria"] = suggestions
            
            return ai_results
            
        except Exception as e:
            logger.error(f"Erro na análise de IA: {e}")
            # Retorna estrutura padrão em caso de erro
            return {
                "feedback_qualitativo": {
                    "pontos_fortes": ["Análise básica concluída"],
                    "pontos_fracos": ["Análise limitada devido a erro no sistema"],
                    "sugestoes": ["Tente novamente mais tarde"]
                },
                "analise_estrutural_ia": {},
                "sugestoes_melhoria": ["Verifique a conexão com a IA"]
            }
    
    def _calculate_comprehensive_scores(
        self, 
        structural_analysis: Dict[str, Any],
        text_structure: Dict[str, Any],
        keyword_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calcula pontuações abrangentes baseadas em todas as análises."""
        try:
            scores = {}
            
            # Função auxiliar para converter pontuações de forma segura
            def safe_convert_score(score_value, default=0.0):
                """Converte pontuação para float de forma segura."""
                if score_value is None:
                    return default
                
                try:
                    # Se já for número, retorna como está
                    if isinstance(score_value, (int, float)):
                        return float(score_value)
                    
                    # Se for string, tenta converter
                    if isinstance(score_value, str):
                        return float(score_value)
                    
                    # Se for outro tipo, retorna padrão
                    return default
                except (ValueError, TypeError):
                    logger.warning(f"Não foi possível converter pontuação '{score_value}' para número. Usando valor padrão {default}")
                    return default
            
            # Pontuação de quantificação
            quant_score_raw = structural_analysis.get("quantificacao", {}).get("score_quantificacao", 0.0)
            quant_score = safe_convert_score(quant_score_raw, 0.0) * 100
            scores["pontuacao_quantificacao"] = round(quant_score, 1)
            
            # Pontuação de verbos de ação
            verbs_score_raw = structural_analysis.get("verbos_de_acao", {}).get("score_verbos", 0.0)
            verbs_score = safe_convert_score(verbs_score_raw, 0.0) * 100
            scores["pontuacao_verbos_acao"] = round(verbs_score, 1)
            
            # Pontuação de estrutura
            if text_structure and "score_estrutura" in text_structure:
                structure_score_raw = text_structure["score_estrutura"]
                structure_score = safe_convert_score(structure_score_raw, 0.0) * 100
                scores["pontuacao_estrutura"] = round(structure_score, 1)
            else:
                scores["pontuacao_estrutura"] = 0.0
            
            # Pontuação de palavras-chave
            if keyword_analysis and "error" not in keyword_analysis:
                keyword_score_raw = keyword_analysis.get("score", 0.0)
                keyword_score = safe_convert_score(keyword_score_raw, 0.0) * 100
                scores["pontuacao_palavras_chave"] = round(keyword_score, 1)
            else:
                scores["pontuacao_palavras_chave"] = 0.0
            
            # Pontuação geral (média ponderada)
            weights = {
                "quantificacao": 0.25,
                "verbos_acao": 0.20,
                "estrutura": 0.30,
                "palavras_chave": 0.25
            }
            
            overall_score = (
                scores["pontuacao_quantificacao"] * weights["quantificacao"] +
                scores["pontuacao_verbos_acao"] * weights["verbos_acao"] +
                scores["pontuacao_estrutura"] * weights["estrutura"] +
                scores["pontuacao_palavras_chave"] * weights["palavras_chave"]
            )
            
            scores["pontuacao_geral"] = round(overall_score, 1)
            scores["nivel"] = self._classify_level(overall_score)
            
            return scores
            
        except Exception as e:
            logger.error(f"Erro no cálculo de pontuações: {e}")
            return {
                "pontuacao_quantificacao": 0.0,
                "pontuacao_verbos_acao": 0.0,
                "pontuacao_estrutura": 0.0,
                "pontuacao_palavras_chave": 0.0,
                "pontuacao_geral": 0.0,
                "nivel": "Erro",
                "error": str(e)
            }
    
    def _generate_recommendations(
        self,
        cv_text: str,
        structural_analysis: Dict[str, Any],
        text_structure: Dict[str, Any],
        keyword_analysis: Dict[str, Any],
        scores: Dict[str, Any]
    ) -> List[str]:
        """Gera recomendações baseadas nos resultados da análise."""
        recommendations = []
        
        try:
            # Recomendações baseadas em quantificação
            if scores.get("pontuacao_quantificacao", 0) < 60:
                recommendations.append("Adicione mais números e métricas quantificáveis ao seu currículo")
            
            # Recomendações baseadas em verbos de ação
            if scores.get("pontuacao_verbos_acao", 0) < 60:
                recommendations.append("Use mais verbos de ação para descrever suas realizações")
            
            # Recomendações baseadas em estrutura
            if scores.get("pontuacao_estrutura", 0) < 70:
                recommendations.append("Melhore a organização e formatação do currículo")
            
            # Recomendações baseadas em palavras-chave
            if scores.get("pontuacao_palavras_chave", 0) < 70:
                recommendations.append("Inclua mais palavras-chave relevantes para a vaga")
            
            # Recomendações baseadas na pontuação geral
            if scores.get("pontuacao_geral", 0) < 70:
                recommendations.append("Considere uma revisão geral do currículo")
            
            # Se não houver recomendações específicas
            if not recommendations:
                recommendations.append("Seu currículo está bem estruturado! Continue assim!")
            
            return recommendations[:5]  # Máximo de 5 recomendações
            
        except Exception as e:
            logger.error(f"Erro ao gerar recomendações: {e}")
            return ["Erro ao gerar recomendações específicas"]
    
    def _consolidate_results(
        self,
        structural_analysis: Dict[str, Any],
        text_structure: Dict[str, Any],
        keyword_analysis: Dict[str, Any],
        ai_feedback: Dict[str, Any],
        scores: Dict[str, Any],
        recommendations: List[str]
    ) -> Dict[str, Any]:
        """Consolida todos os resultados em uma estrutura unificada."""
        # Extrai dados do feedback da IA
        feedback_data = ai_feedback.get("feedback_qualitativo", {})
        if isinstance(feedback_data, dict):
            pontos_fortes = feedback_data.get("pontos_fortes", ["Análise concluída com sucesso"])
            pontos_fracos = feedback_data.get("pontos_fracos", ["Verifique as sugestões de melhoria"])
            sugestoes = feedback_data.get("sugestoes", recommendations if recommendations else ["Continue melhorando seu currículo"])
        else:
            pontos_fortes = ["Análise concluída com sucesso"]
            pontos_fracos = ["Verifique as sugestões de melhoria"]
            sugestoes = recommendations if recommendations else ["Continue melhorando seu currículo"]
        
        return {
            "feedback_qualitativo": {
                "pontos_fortes": pontos_fortes,
                "pontos_fracos": pontos_fracos,
                "sugestoes": sugestoes
            },
            "quantificacao": structural_analysis.get("quantificacao", {
                "total": 0,
                "items": [],
                "score_quantificacao": 0.0
            }),
            "verbos_de_acao": structural_analysis.get("verbos_de_acao", {
                "total": 0,
                "items": [],
                "score_verbos": 0.0
            }),
            "pontuacoes": {
                "pontuacao_quantificacao": scores.get("pontuacao_quantificacao", 0.0),
                "pontuacao_verbos_acao": scores.get("pontuacao_verbos_acao", 0.0),
                "pontuacao_estrutura": scores.get("pontuacao_estrutura", 0.0),
                "pontuacao_palavras_chave": scores.get("pontuacao_palavras_chave", 0.0),
                "pontuacao_geral": scores.get("pontuacao_geral", 0.0)
            },
            "palavras_chave": keyword_analysis if "error" not in keyword_analysis else {
                "score": 0.0,
                "items": [],
                "correspondencia": 0.0
            },
            "analise_estrutural": structural_analysis,
            "analise_texto": text_structure,
            "resumo": {
                "nivel_geral": scores.get("nivel", "N/A"),
                "pontuacao_geral": scores.get("pontuacao_geral", 0.0),
                "ferramentas_ai_disponiveis": self.gemini_client.is_configured,
                "spacy_disponivel": self.analysis_engine.spacy_available
            }
        }
    
    def _classify_level(self, score: float) -> str:
        """Classifica o nível baseado na pontuação."""
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
    
    def _get_used_tools(self) -> Dict[str, bool]:
        """Retorna informações sobre as ferramentas utilizadas."""
        return {
            "spacy": self.analysis_engine.spacy_available,
            "gemini": self.gemini_client.is_configured,
            "regex": True,  # Sempre disponível
            "estrutural": True  # Sempre disponível
        }
    
    def _empty_analysis_result(self) -> Dict[str, Any]:
        """Retorna resultado vazio para análise."""
        return {
            "error": "Texto do currículo está vazio",
            "analise_estrutural": {},
            "analise_texto": {},
            "analise_palavras_chave": {},
            "feedback_ia": {},
            "pontuacoes": {},
            "recomendacoes": [],
            "resumo": {},
            "metadados": {}
        }
    
    def _error_analysis_result(self, error_message: str) -> Dict[str, Any]:
        """Retorna resultado de erro para análise."""
        return {
            "error": error_message,
            "analise_estrutural": {},
            "analise_texto": {},
            "analise_palavras_chave": {},
            "feedback_ia": {},
            "pontuacoes": {},
            "recomendacoes": [],
            "resumo": {},
            "metadados": {}
        }
    
    async def get_analysis_summary(self, cv_text: str) -> Dict[str, Any]:
        """
        Retorna um resumo rápido da análise do currículo.
        
        Args:
            cv_text: Texto do currículo
            
        Returns:
            Resumo da análise
        """
        if not cv_text:
            return {"error": "Texto vazio"}
        
        try:
            # Análise rápida usando métodos assíncronos
            quantification = await self._analyze_quantification_sync(cv_text)
            action_verbs = await self._analyze_action_verbs_sync(cv_text)
            
            # Função auxiliar para converter pontuações de forma segura
            def safe_convert_score(score_value, default=0.0):
                """Converte pontuação para float de forma segura."""
                if score_value is None:
                    return default
                
                try:
                    # Se já for número, retorna como está
                    if isinstance(score_value, (int, float)):
                        return float(score_value)
                    
                    # Se for string, tenta converter
                    if isinstance(score_value, str):
                        return float(score_value)
                    
                    # Se for outro tipo, retorna padrão
                    return default
                except (ValueError, TypeError):
                    logger.warning(f"Não foi possível converter pontuação '{score_value}' para número. Usando valor padrão {default}")
                    return default
            
            # Cálculo de score básico com conversão segura
            quant_score = safe_convert_score(quantification.get("score_quantificacao", 0.0), 0.0)
            verbs_score = safe_convert_score(action_verbs.get("score_verbos", 0.0), 0.0)
            
            basic_score = (quant_score * 0.6 + verbs_score * 0.4) * 100
            
            return {
                "score_rapido": round(basic_score, 1),
                "nivel": self._classify_level(basic_score),
                "quantificacao": len(quantification.get("items", [])),
                "verbos_acao": len(action_verbs.get("items", [])),
                "ferramentas_disponiveis": self._get_used_tools()
            }
            
        except Exception as e:
            logger.error(f"Erro no resumo rápido: {e}")
            return {"error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Verifica a saúde de todas as ferramentas de análise."""
        return {
            "status": "operacional",
            "ferramentas": {
                "spacy": {
                    "disponivel": self.analysis_engine.spacy_available,
                    "modelo": getattr(self.analysis_engine, 'nlp', None) is not None
                },
                "gemini": {
                    "disponivel": self.gemini_client.is_configured,
                    "api_key": bool(self.gemini_client.api_key)
                },
                "regex": True,
                "estrutural": True
            },
            "timestamp": time.time()
        }
