"""
Teste da funcionalidade de análise de currículos.

Este arquivo testa as funções de análise sem depender do FastAPI.
"""

import asyncio
import json
from app.agno import (
    analisar_quantificacao,
    analisar_verbos_de_acao,
    calcular_pontuacoes,
    analisar_palavras_chave,
    analisar_curriculo_completo
)

def test_analise_basica():
    """Testa as funções básicas de análise."""
    
    # Texto de exemplo de currículo
    texto_cv = """
    Desenvolvedor Python com 5 anos de experiência.
    
    EXPERIÊNCIA PROFISSIONAL:
    - Desenvolvi e implementei 3 sistemas web usando Django e React
    - Liderou uma equipe de 4 desenvolvedores
    - Aumentei a performance da aplicação em 40%
    - Reduzi o tempo de deploy de 2 horas para 15 minutos
    - Gerenciou projetos com orçamento de R$ 500.000
    
    TECNOLOGIAS:
    Python, Django, React, PostgreSQL, AWS, Docker
    
    FORMAÇÃO:
    Bacharel em Ciência da Computação - UFMG (2018-2022)
    """
    
    print("🧪 Testando análise básica...")
    print("=" * 50)
    
    # Testa análise de quantificação
    print("\n📊 Análise de Quantificação:")
    analise_quant = analisar_quantificacao(texto_cv)
    print(json.dumps(analise_quant, indent=2, ensure_ascii=False))
    
    # Testa análise de verbos de ação
    print("\n🏃 Análise de Verbos de Ação:")
    analise_verbos = analisar_verbos_de_acao(texto_cv)
    print(json.dumps(analise_verbos, indent=2, ensure_ascii=False))
    
    # Testa cálculo de pontuações
    print("\n⭐ Cálculo de Pontuações:")
    pontuacoes = calcular_pontuacoes(analise_quant, analise_verbos)
    print(json.dumps(pontuacoes, indent=2, ensure_ascii=False))
    
    # Testa análise de palavras-chave
    print("\n🔑 Análise de Palavras-Chave:")
    descricao_vaga = "Desenvolvedor Python com experiência em Django, React e AWS"
    palavras_chave = analisar_palavras_chave(texto_cv, descricao_vaga)
    print(json.dumps(palavras_chave, indent=2, ensure_ascii=False))
    
    # Testa análise completa
    print("\n🎯 Análise Completa:")
    analise_completa = analisar_curriculo_completo(texto_cv, descricao_vaga)
    print(json.dumps(analise_completa, indent=2, ensure_ascii=False))

def test_curriculo_vazio():
    """Testa comportamento com currículo vazio."""
    
    print("\n🧪 Testando currículo vazio...")
    print("=" * 50)
    
    texto_vazio = ""
    
    analise_quant = analisar_quantificacao(texto_vazio)
    analise_verbos = analisar_verbos_de_acao(texto_vazio)
    pontuacoes = calcular_pontuacoes(analise_quant, analise_verbos)
    
    print("📊 Análise de Quantificação (vazio):")
    print(json.dumps(analise_quant, indent=2, ensure_ascii=False))
    
    print("\n🏃 Análise de Verbos (vazio):")
    print(json.dumps(analise_verbos, indent=2, ensure_ascii=False))
    
    print("\n⭐ Pontuações (vazio):")
    print(json.dumps(pontuacoes, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    print("🚀 Iniciando testes de análise de currículos...")
    print("=" * 60)
    
    try:
        test_analise_basica()
        test_curriculo_vazio()
        
        print("\n✅ Todos os testes foram executados com sucesso!")
        print("\n💡 Para testar a API completa, execute:")
        print("   uv run uvicorn main:app --reload")
        print("\n📚 Documentação da API disponível em:")
        print("   http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        print("\n🔧 Verifique se:")
        print("   1. Todas as dependências estão instaladas (uv sync)")
        print("   2. O modelo spaCy está instalado (python -m spacy download pt_core_news_sm)")
        print("   3. As variáveis de ambiente estão configuradas (.env)")
