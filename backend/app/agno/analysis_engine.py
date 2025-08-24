"""
Motor de Análise para Currículos

Este módulo integra spaCy e outras ferramentas de análise para fornecer
análises estruturais e quantitativas dos currículos.
"""

import re
import logging
from typing import Dict, List, Any, Tuple
import spacy
from app.core.config import settings

logger = logging.getLogger(__name__)


class AnalysisEngine:
    """Motor de análise que integra múltiplas ferramentas de análise."""
    
    def __init__(self):
        """Inicializa o motor de análise."""
        self.spacy_available = self._initialize_spacy()
        self._setup_analysis_tools()
    
    def _initialize_spacy(self) -> bool:
        """Inicializa o spaCy e verifica disponibilidade."""
        try:
            self.nlp = spacy.load(settings.spacy_model)
            logger.info(f"Modelo spaCy carregado: {settings.spacy_model}")
            return True
        except OSError:
            logger.warning(f"Modelo spaCy não encontrado: {settings.spacy_model}")
            logger.info("Usando análises alternativas baseadas em regex")
            self.nlp = None
            return False
        except Exception as e:
            logger.error(f"Erro ao inicializar spaCy: {e}")
            self.nlp = None
            return False
    
    def _setup_analysis_tools(self):
        """Configura ferramentas de análise alternativas."""
        # Verbos de ação comuns em currículos
        self.action_verbs = {
            'desenvolver', 'implementar', 'criar', 'construir', 'liderar', 'gerenciar',
            'otimizar', 'melhorar', 'aumentar', 'reduzir', 'analisar', 'resolver',
            'coordenar', 'supervisionar', 'treinar', 'mentorar', 'planejar', 'executar',
            'monitorar', 'avaliar', 'testar', 'deployar', 'configurar', 'manter',
            'desenvolveu', 'implementou', 'criou', 'construiu', 'liderou', 'gerenciou',
            'otimizou', 'melhorou', 'aumentou', 'reduziu', 'analisou', 'resolvia',
            'coordenou', 'supervisionou', 'treinou', 'mentorou', 'planejou', 'executou',
            'monitorou', 'avaliou', 'testou', 'deployou', 'configurou', 'manteve'
        }
        
        # Padrões de quantificação
        self.quantification_patterns = {
            'percentages': r'\b\d+(?:\.\d+)?%\b',
            'currency': r'R?\$?\s*\d+(?:,\d{3})*(?:\.\d{2})?',
            'numbers': r'\b\d+(?:\.\d+)?\b',
            'ranges': r'\d+\s*[-–]\s*\d+',
            'ratios': r'\d+:\d+',
            'years': r'\b(?:19|20)\d{2}\b'
        }
    
    def analyze_quantification(self, text: str) -> Dict[str, Any]:
        """
        Analisa quantificação no currículo.
        
        Args:
            text: Texto do currículo
            
        Returns:
            Análise de quantificação
        """
        if not text:
            return self._empty_quantification_result()
        
        if self.spacy_available:
            return self._analyze_quantification_spacy(text)
        else:
            return self._analyze_quantification_regex(text)
    
    def _analyze_quantification_spacy(self, text: str) -> Dict[str, Any]:
        """Análise de quantificação usando spaCy."""
        try:
            doc = self.nlp(text)
            
            numbers = []
            percentages = []
            currency_values = []
            quantities = []
            ranges = []
            ratios = []
            years = []
            
            for token in doc:
                # Números simples
                if token.like_num:
                    numbers.append(token.text)
                
                # Percentuais
                if "%" in token.text:
                    percentages.append(token.text)
                
                # Valores monetários
                if any(symbol in token.text for symbol in ["R$", "$", "€", "USD", "EUR"]):
                    currency_values.append(token.text)
                
                # Quantidades com unidades
                if token.like_num and token.nbor().is_alpha:
                    quantities.append(f"{token.text} {token.nbor().text}")
            
            # Análise de contexto para ranges e ratios
            for i, token in enumerate(doc):
                if token.like_num and i + 1 < len(doc):
                    next_token = doc[i + 1]
                    if next_token.text in ["-", "–", ":", "a", "até"]:
                        if i + 2 < len(doc) and doc[i + 2].like_num:
                            if next_token.text in ["-", "–", "a", "até"]:
                                ranges.append(f"{token.text}{next_token.text}{doc[i + 2].text}")
                            elif next_token.text == ":":
                                ratios.append(f"{token.text}:{doc[i + 2].text}")
            
            # Análise de anos
            for token in doc:
                if token.like_num and len(token.text) == 4:
                    year = int(token.text)
                    if 1900 <= year <= 2030:
                        years.append(token.text)
            
            score = self._calculate_quantification_score(
                len(numbers), len(percentages), len(currency_values), 
                len(quantities), len(ranges), len(ratios), len(years)
            )
            
            return {
                "numeros_encontrados": numbers,
                "percentuais": percentages,
                "valores_monetarios": currency_values,
                "quantidades": quantities,
                "ranges": ranges,
                "ratios": ratios,
                "anos": years,
                "score_quantificacao": score,
                "metodo_analise": "spaCy"
            }
            
        except Exception as e:
            logger.error(f"Erro na análise spaCy: {e}")
            return self._analyze_quantification_regex(text)
    
    def _analyze_quantification_regex(self, text: str) -> Dict[str, Any]:
        """Análise de quantificação usando regex."""
        try:
            numbers = re.findall(self.quantification_patterns['numbers'], text)
            percentages = re.findall(self.quantification_patterns['percentages'], text)
            currency_values = re.findall(self.quantification_patterns['currency'], text)
            ranges = re.findall(self.quantification_patterns['ranges'], text)
            ratios = re.findall(self.quantification_patterns['ratios'], text)
            years = re.findall(self.quantification_patterns['years'], text)
            
            # Quantidades com unidades (padrão simples)
            quantities = []
            for match in re.finditer(r'\b(\d+)\s+([a-zA-Z]+)\b', text):
                quantities.append(f"{match.group(1)} {match.group(2)}")
            
            score = self._calculate_quantification_score(
                len(numbers), len(percentages), len(currency_values),
                len(quantities), len(ranges), len(ratios), len(years)
            )
            
            return {
                "numeros_encontrados": numbers,
                "percentuais": percentages,
                "valores_monetarios": currency_values,
                "quantidades": quantities,
                "ranges": ranges,
                "ratios": ratios,
                "anos": years,
                "score_quantificacao": score,
                "metodo_analise": "regex"
            }
            
        except Exception as e:
            logger.error(f"Erro na análise regex: {e}")
            return self._empty_quantification_result()
    
    def _calculate_quantification_score(self, *counts) -> float:
        """Calcula score de quantificação baseado nos diferentes tipos encontrados."""
        total_items = sum(counts)
        diversity_bonus = len([c for c in counts if c > 0]) * 0.1
        
        base_score = min(total_items * 0.15, 0.8)
        final_score = min(base_score + diversity_bonus, 1.0)
        
        return round(final_score, 3)
    
    def _empty_quantification_result(self) -> Dict[str, Any]:
        """Retorna resultado vazio para quantificação."""
        return {
            "numeros_encontrados": [],
            "percentuais": [],
            "valores_monetarios": [],
            "quantidades": [],
            "ranges": [],
            "ratios": [],
            "anos": [],
            "score_quantificacao": 0.0,
            "metodo_analise": "nenhum"
        }
    
    def analyze_action_verbs(self, text: str) -> Dict[str, Any]:
        """
        Analisa verbos de ação no currículo.
        
        Args:
            text: Texto do currículo
            
        Returns:
            Análise de verbos de ação
        """
        if not text:
            return self._empty_verbs_result()
        
        if self.spacy_available:
            return self._analyze_verbs_spacy(text)
        else:
            return self._analyze_verbs_regex(text)
    
    def _analyze_verbs_spacy(self, text: str) -> Dict[str, Any]:
        """Análise de verbos usando spaCy."""
        try:
            doc = self.nlp(text)
            
            all_verbs = []
            action_verbs = []
            verb_forms = {}
            
            for token in doc:
                if token.pos_ == "VERB":
                    lemma = token.lemma_.lower()
                    all_verbs.append(token.text)
                    
                    if lemma in self.action_verbs:
                        action_verbs.append(token.text)
                    
                    # Conta diferentes formas do verbo
                    if lemma not in verb_forms:
                        verb_forms[lemma] = []
                    verb_forms[lemma].append(token.text)
            
            score = self._calculate_verbs_score(len(action_verbs), len(all_verbs))
            
            return {
                "verbos_encontrados": all_verbs,
                "verbos_acao": action_verbs,
                "formas_verbais": verb_forms,
                "score_verbos": score,
                "metodo_analise": "spaCy"
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de verbos spaCy: {e}")
            return self._analyze_verbs_regex(text)
    
    def _analyze_verbs_regex(self, text: str) -> Dict[str, Any]:
        """Análise de verbos usando regex."""
        try:
            text_lower = text.lower()
            all_verbs = []
            action_verbs = []
            
            # Busca por verbos de ação conhecidos
            for verb in self.action_verbs:
                if verb in text_lower:
                    action_verbs.append(verb)
            
            # Busca por padrões de verbos em português
            verb_patterns = [
                r'\b\w+(?:ei|ou|ou|amos|aram|ava|ávamos|avam)\b',  # Passado
                r'\b\w+(?:o|a|amos|am|em)\b',  # Presente
                r'\b\w+(?:ei|á|emos|ão|ia|íamos|iam)\b'  # Futuro/Condicional
            ]
            
            for pattern in verb_patterns:
                matches = re.findall(pattern, text_lower)
                all_verbs.extend(matches)
            
            # Remove duplicatas
            all_verbs = list(set(all_verbs))
            action_verbs = list(set(action_verbs))
            
            score = self._calculate_verbs_score(len(action_verbs), len(all_verbs))
            
            return {
                "verbos_encontrados": all_verbs,
                "verbos_acao": action_verbs,
                "formas_verbais": {},
                "score_verbos": score,
                "metodo_analise": "regex"
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de verbos regex: {e}")
            return self._empty_verbs_result()
    
    def _calculate_verbs_score(self, action_count: int, total_count: int) -> float:
        """Calcula score de verbos baseado na proporção de verbos de ação."""
        if total_count == 0:
            return 0.0
        
        action_ratio = action_count / total_count
        diversity_bonus = min(total_count * 0.05, 0.3)
        
        final_score = min(action_ratio + diversity_bonus, 1.0)
        return round(final_score, 3)
    
    def _empty_verbs_result(self) -> Dict[str, Any]:
        """Retorna resultado vazio para verbos."""
        return {
            "verbos_encontrados": [],
            "verbos_acao": [],
            "formas_verbais": {},
            "score_verbos": 0.0,
            "metodo_analise": "nenhum"
        }
    
    def analyze_text_structure(self, text: str) -> Dict[str, Any]:
        """
        Analisa a estrutura geral do texto.
        
        Args:
            text: Texto do currículo
            
        Returns:
            Análise da estrutura do texto
        """
        if not text:
            return {"error": "Texto vazio"}
        
        try:
            lines = text.split('\n')
            paragraphs = text.split('\n\n')
            
            # Análise de seções
            sections = self._identify_sections(lines)
            
            # Análise de formatação
            formatting = self._analyze_formatting(text)
            
            # Análise de comprimento
            length_analysis = self._analyze_length(text, lines, paragraphs)
            
            return {
                "secoes": sections,
                "formatacao": formatting,
                "comprimento": length_analysis,
                "estrutura_geral": self._evaluate_structure_quality(sections, formatting, length_analysis)
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de estrutura: {e}")
            return {"error": f"Erro na análise: {str(e)}"}
    
    def _identify_sections(self, lines: List[str]) -> Dict[str, Any]:
        """Identifica seções comuns em currículos."""
        sections = {
            "dados_pessoais": [],
            "experiencia": [],
            "educacao": [],
            "habilidades": [],
            "projetos": [],
            "certificacoes": [],
            "idiomas": []
        }
        
        section_keywords = {
            "dados_pessoais": ["nome", "email", "telefone", "endereço", "linkedin"],
            "experiencia": ["experiência", "trabalho", "empresa", "cargo", "função"],
            "educacao": ["educação", "formação", "graduação", "curso", "universidade"],
            "habilidades": ["habilidades", "skills", "competências", "tecnologias"],
            "projetos": ["projetos", "portfólio", "trabalhos", "desenvolvimento"],
            "certificacoes": ["certificações", "certificados", "cursos", "treinamentos"],
            "idiomas": ["idiomas", "inglês", "espanhol", "francês"]
        }
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    sections[section].append({
                        "linha": i + 1,
                        "conteudo": line.strip(),
                        "confianca": 0.8
                    })
        
        return sections
    
    def _analyze_formatting(self, text: str) -> Dict[str, Any]:
        """Analisa a formatação do texto."""
        return {
            "maiusculas": len(re.findall(r'[A-Z]', text)),
            "minusculas": len(re.findall(r'[a-z]', text)),
            "numeros": len(re.findall(r'\d', text)),
            "pontuacao": len(re.findall(r'[.,;:!?]', text)),
            "quebras_linha": text.count('\n'),
            "espacos_duplos": len(re.findall(r'  +', text))
        }
    
    def _analyze_length(self, text: str, lines: List[str], paragraphs: List[str]) -> Dict[str, Any]:
        """Analisa o comprimento do texto."""
        return {
            "total_caracteres": len(text),
            "total_palavras": len(text.split()),
            "total_linhas": len(lines),
            "total_paragrafos": len(paragraphs),
            "media_palavras_linha": len(text.split()) / max(len(lines), 1),
            "media_palavras_paragrafo": len(text.split()) / max(len(paragraphs), 1)
        }
    
    def _evaluate_structure_quality(self, sections: Dict, formatting: Dict, length: Dict) -> Dict[str, Any]:
        """Avalia a qualidade geral da estrutura."""
        # Score baseado na presença de seções
        section_score = len([s for s in sections.values() if s]) / len(sections) * 100
        
        # Score baseado na formatação
        formatting_score = 100
        if formatting.get("espacos_duplos", 0) > 5:
            formatting_score -= 20
        if formatting.get("quebras_linha", 0) < 10:
            formatting_score -= 30
        
        # Score baseado no comprimento
        length_score = 100
        if length.get("total_palavras", 0) < 100:
            length_score -= 40
        elif length.get("total_palavras", 0) > 1000:
            length_score -= 20
        
        overall_score = (section_score + formatting_score + length_score) / 3
        
        return {
            "score_secoes": round(section_score, 1),
            "score_formatacao": round(formatting_score, 1),
            "score_comprimento": round(length_score, 1),
            "score_geral": round(overall_score, 1),
            "nivel": self._classify_level(overall_score)
        }
    
    def _classify_level(self, score: float) -> str:
        """Classifica o nível baseado no score."""
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
