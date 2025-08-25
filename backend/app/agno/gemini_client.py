"""
Cliente do Google Gemini para análise de currículos

Este módulo gerencia todas as interações com a API do Google Gemini,
incluindo configuração, prompts otimizados e tratamento de erros.
"""

import os
import logging
from typing import Dict, Any, Optional, List
import google.generativeai as genai
from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiClient:
    """Cliente para interação com a API do Google Gemini."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o cliente Gemini.
        
        Args:
            api_key: Chave da API do Gemini. Se não fornecida, usa a das configurações.
        """
        self.api_key = api_key or settings.gemini_api_key
        
        if not self.api_key:
            logger.warning("Chave da API do Gemini não configurada")
            self._configured = False
            return
            
        try:
            genai.configure(api_key=self.api_key)
            self._configured = True
            logger.info("Cliente Gemini configurado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao configurar cliente Gemini: {e}")
            self._configured = False
    
    @property
    def is_configured(self) -> bool:
        """Verifica se o cliente está configurado."""
        return self._configured
    
    async def analyze_curriculum_structure(self, text: str) -> Dict[str, Any]:
        """
        Analisa a estrutura do currículo usando Gemini.
        
        Args:
            text: Texto do currículo
            
        Returns:
            Análise estrutural do currículo
        """
        if not self._configured:
            return {"error": "Cliente Gemini não configurado"}
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Analise a estrutura do seguinte currículo e forneça uma análise detalhada em formato JSON.
            
            Analise:
            1. Organização e clareza
            2. Presença de seções essenciais
            3. Qualidade da apresentação
            4. Profissionalismo
            
            Retorne apenas um JSON válido com a seguinte estrutura:
            {{
                "estrutura": {{
                    "organizacao": "score de 0-100",
                    "clareza": "score de 0-100", 
                    "secoes_essenciais": "score de 0-100",
                    "apresentacao": "score de 0-100",
                    "profissionalismo": "score de 0-100"
                }},
                "pontos_fortes": ["lista de pontos fortes"],
                "areas_melhoria": ["lista de áreas para melhorar"],
                "score_geral": "score de 0-100"
            }}
            
            Texto do currículo:
            {text[:2000]}...
            """
            
            # Verifica se o método é assíncrono ou síncrono
            try:
                if hasattr(model, 'generate_content_async'):
                    response = await model.generate_content_async(prompt)
                else:
                    response = model.generate_content(prompt)
            except Exception as api_error:
                logger.error(f"Erro na API Gemini: {api_error}")
                return {"error": f"Erro na API Gemini: {str(api_error)}"}
                
            return self._parse_gemini_response(response.text)
            
        except Exception as e:
            logger.error(f"Erro na análise estrutural: {e}")
            return {"error": f"Erro na análise: {str(e)}"}
    
    async def generate_qualitative_feedback(self, text: str, job_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Gera feedback qualitativo sobre o currículo.
        
        Args:
            text: Texto do currículo
            job_description: Descrição da vaga (opcional)
            
        Returns:
            Feedback qualitativo estruturado
        """
        if not self._configured:
            return {
                "pontos_fortes": ["Análise básica concluída"],
                "pontos_fracos": ["Cliente Gemini não configurado"],
                "sugestoes": ["Configure a chave da API do Gemini"]
            }
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if job_description:
                prompt = f"""
                Analise o currículo em relação à descrição da vaga e forneça feedback construtivo.
                
                Descrição da Vaga:
                {job_description}
                
                Currículo:
                {text[:1500]}...
                
                Retorne apenas um JSON válido com a seguinte estrutura:
                {{
                    "pontos_fortes": ["lista de 2-3 pontos fortes do candidato"],
                    "pontos_fracos": ["lista de 2-3 pontos fracos ou áreas para melhorar"],
                    "sugestoes": ["lista de 2-3 sugestões específicas de melhoria"]
                }}
                """
            else:
                prompt = f"""
                Analise o seguinte currículo e forneça um feedback construtivo.
                
                Foque em:
                1. Pontos fortes do candidato
                2. Qualidade geral da apresentação
                3. Sugestões de melhoria
                
                Currículo:
                {text[:1500]}...
                
                Retorne apenas um JSON válido com a seguinte estrutura:
                {{
                    "pontos_fortes": ["lista de 2-3 pontos fortes do candidato"],
                    "pontos_fracos": ["lista de 2-3 pontos fracos ou áreas para melhorar"],
                    "sugestoes": ["lista de 2-3 sugestões específicas de melhoria"]
                }}
                """
            
            # Verifica se o método é assíncrono ou síncrono
            try:
                if hasattr(model, 'generate_content_async'):
                    response = await model.generate_content_async(prompt)
                else:
                    response = model.generate_content(prompt)
            except Exception as api_error:
                logger.error(f"Erro na API Gemini: {api_error}")
                return {
                    "pontos_fortes": ["Análise básica concluída"],
                    "pontos_fracos": [f"Erro na API: {str(api_error)}"],
                    "sugestoes": ["Tente novamente mais tarde"]
                }
                
            parsed_response = self._parse_gemini_response(response.text)
            
            # Se a resposta não for um dicionário válido, retorna estrutura padrão
            if isinstance(parsed_response, dict) and "pontos_fortes" in parsed_response:
                return parsed_response
            else:
                # Fallback para estrutura padrão
                return {
                    "pontos_fortes": ["Análise concluída com sucesso"],
                    "pontos_fracos": ["Verifique as sugestões de melhoria"],
                    "sugestoes": ["Continue melhorando seu currículo"]
                }
            
        except Exception as e:
            logger.error(f"Erro ao gerar feedback: {e}")
            # Retorna estrutura padrão em caso de erro
            return {
                "pontos_fortes": ["Análise básica concluída"],
                "pontos_fracos": ["Erro na análise da IA"],
                "sugestoes": ["Tente novamente mais tarde"]
            }
    
    async def analyze_keywords_match(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """
        Analisa a correspondência de palavras-chave entre currículo e vaga.
        
        Args:
            cv_text: Texto do currículo
            job_description: Descrição da vaga
            
        Returns:
            Análise de correspondência de palavras-chave
        """
        if not self._configured:
            return {
                "score": 0.0,
                "items": [],
                "correspondencia": 0.0,
                "error": "Cliente Gemini não configurado"
            }
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Analise a correspondência entre o currículo e a descrição da vaga.
            
            Descrição da Vaga:
            {job_description}
            
            Currículo:
            {cv_text[:1500]}...
            
            Retorne apenas um JSON válido com a seguinte estrutura:
            {{
                "score": "score de 0.0 a 1.0",
                "items": ["lista de palavras-chave encontradas"],
                "correspondencia": "score de 0-100",
                "palavras_chave_encontradas": ["lista de palavras-chave encontradas"],
                "palavras_chave_faltantes": ["lista de palavras-chave importantes que faltam"],
                "recomendacoes": ["lista de recomendações para melhorar a correspondência"]
            }}
            """
            
            # Verifica se o método é assíncrono ou síncrono
            try:
                if hasattr(model, 'generate_content_async'):
                    response = await model.generate_content_async(prompt)
                else:
                    response = model.generate_content(prompt)
            except Exception as api_error:
                logger.error(f"Erro na API Gemini: {api_error}")
                return {
                    "score": 0.0,
                    "items": [],
                    "correspondencia": 0.0,
                    "error": f"Erro na API Gemini: {str(api_error)}"
                }
                
            parsed_response = self._parse_gemini_response(response.text)
            
            # Se a resposta não for um dicionário válido, retorna estrutura padrão
            if isinstance(parsed_response, dict) and "score" in parsed_response:
                return parsed_response
            else:
                # Fallback para análise simples
                return self._simple_keyword_analysis_fallback(cv_text, job_description)
            
        except Exception as e:
            logger.error(f"Erro na análise de palavras-chave: {e}")
            # Fallback para análise simples
            return self._simple_keyword_analysis_fallback(cv_text, job_description)
    
    def _simple_keyword_analysis_fallback(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Análise simples de palavras-chave como fallback."""
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
            "items": found_keywords[:10],
            "correspondencia": round(score * 100, 1),
            "palavras_chave_encontradas": found_keywords,
            "palavras_chave_faltantes": missing_keywords,
            "recomendacoes": ["Inclua mais palavras-chave relevantes para a vaga"]
        }
    
    async def generate_improvement_suggestions(self, cv_text: str, analysis_results: Dict[str, Any]) -> List[str]:
        """
        Gera sugestões específicas de melhoria baseadas nos resultados da análise.
        
        Args:
            cv_text: Texto do currículo
            analysis_results: Resultados das análises anteriores
            
        Returns:
            Lista de sugestões de melhoria
        """
        if not self._configured:
            return ["Cliente Gemini não configurado"]
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Com base na análise do currículo, gere 5 sugestões específicas e acionáveis para melhorar o currículo.
            
            Resultados da Análise:
            {str(analysis_results)}
            
            Currículo:
            {cv_text[:1000]}...
            
            Forneça apenas uma lista numerada de sugestões práticas e específicas.
            Cada sugestão deve ser clara e implementável.
            """
            
            # Verifica se o método é assíncrono ou síncrono
            try:
                if hasattr(model, 'generate_content_async'):
                    response = await model.generate_content_async(prompt)
                else:
                    response = model.generate_content(prompt)
            except Exception as api_error:
                logger.error(f"Erro na API Gemini: {api_error}")
                return [f"Erro ao gerar sugestões: {str(api_error)}"]
                
            suggestions = response.text.strip().split('\n')
            
            # Filtra e limpa as sugestões
            cleaned_suggestions = []
            for suggestion in suggestions:
                suggestion = suggestion.strip()
                if suggestion and not suggestion.startswith('#'):
                    # Remove numeração se existir
                    if suggestion[0].isdigit() and '.' in suggestion[:3]:
                        suggestion = suggestion.split('.', 1)[1].strip()
                    cleaned_suggestions.append(suggestion)
            
            return cleaned_suggestions[:5]  # Retorna no máximo 5 sugestões
            
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões: {e}")
            return [f"Erro ao gerar sugestões: {str(e)}"]
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """
        Tenta fazer o parse da resposta do Gemini como JSON.
        
        Args:
            response_text: Texto da resposta
            
        Returns:
            Dicionário parseado ou erro
        """
        try:
            import json
            # Remove possíveis prefixos ou sufixos não-JSON
            text = response_text.strip()
            if text.startswith('```json'):
                text = text[7:]
            if text.endswith('```'):
                text = text[:-3]
            
            return json.loads(text.strip())
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao fazer parse da resposta JSON: {e}")
            logger.error(f"Resposta recebida: {response_text}")
            return {"error": "Resposta inválida do Gemini", "raw_response": response_text}
        except Exception as e:
            logger.error(f"Erro inesperado ao fazer parse: {e}")
            return {"error": f"Erro inesperado: {str(e)}"}
