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
    
    def analyze_curriculum_structure(self, text: str) -> Dict[str, Any]:
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
            model = genai.GenerativeModel('gemini-pro')
            
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
            
            response = model.generate_content(prompt)
            return self._parse_gemini_response(response.text)
            
        except Exception as e:
            logger.error(f"Erro na análise estrutural: {e}")
            return {"error": f"Erro na análise: {str(e)}"}
    
    def generate_qualitative_feedback(self, text: str, job_description: Optional[str] = None) -> str:
        """
        Gera feedback qualitativo sobre o currículo.
        
        Args:
            text: Texto do currículo
            job_description: Descrição da vaga (opcional)
            
        Returns:
            Feedback qualitativo em texto
        """
        if not self._configured:
            return "Cliente Gemini não configurado"
        
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            if job_description:
                prompt = f"""
                Analise o currículo em relação à descrição da vaga e forneça feedback construtivo.
                
                Descrição da Vaga:
                {job_description}
                
                Currículo:
                {text[:1500]}...
                
                Forneça um feedback em até 150 palavras, incluindo:
                1. Pontos fortes do candidato
                2. Como o currículo se alinha com a vaga
                3. Uma sugestão principal de melhoria
                4. Recomendação geral
                """
            else:
                prompt = f"""
                Analise o seguinte currículo e forneça um feedback construtivo em até 150 palavras.
                
                Foque em:
                1. Pontos fortes do candidato
                2. Qualidade geral da apresentação
                3. Uma sugestão principal de melhoria
                4. Recomendação geral
                
                Currículo:
                {text[:1500]}...
                """
            
            response = model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Erro ao gerar feedback: {e}")
            return f"Erro ao gerar feedback: {str(e)}"
    
    def analyze_keywords_match(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """
        Analisa a correspondência de palavras-chave entre currículo e vaga.
        
        Args:
            cv_text: Texto do currículo
            job_description: Descrição da vaga
            
        Returns:
            Análise de correspondência de palavras-chave
        """
        if not self._configured:
            return {"error": "Cliente Gemini não configurado"}
        
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            Analise a correspondência entre o currículo e a descrição da vaga.
            
            Descrição da Vaga:
            {job_description}
            
            Currículo:
            {cv_text[:1500]}...
            
            Retorne apenas um JSON válido com a seguinte estrutura:
            {{
                "palavras_chave_encontradas": ["lista de palavras-chave encontradas"],
                "palavras_chave_faltantes": ["lista de palavras-chave importantes que faltam"],
                "score_correspondencia": "score de 0-100",
                "recomendacoes": ["lista de recomendações para melhorar a correspondência"]
            }}
            """
            
            response = model.generate_content(prompt)
            return self._parse_gemini_response(response.text)
            
        except Exception as e:
            logger.error(f"Erro na análise de palavras-chave: {e}")
            return {"error": f"Erro na análise: {str(e)}"}
    
    def generate_improvement_suggestions(self, cv_text: str, analysis_results: Dict[str, Any]) -> List[str]:
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
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            Com base na análise do currículo, gere 5 sugestões específicas e acionáveis para melhorar o currículo.
            
            Resultados da Análise:
            {str(analysis_results)}
            
            Currículo:
            {cv_text[:1000]}...
            
            Forneça apenas uma lista numerada de sugestões práticas e específicas.
            Cada sugestão deve ser clara e implementável.
            """
            
            response = model.generate_content(prompt)
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
