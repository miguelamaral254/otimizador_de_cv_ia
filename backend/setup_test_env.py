"""
Script para configurar o ambiente de testes.

Este script instala o modelo spaCy necessário e configura o ambiente.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Executa um comando e exibe o resultado."""
    print(f"\n🔧 {description}...")
    print(f"Executando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído com sucesso!")
        if result.stdout:
            print(f"Saída: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao {description.lower()}:")
        print(f"Comando: {e.cmd}")
        print(f"Código de saída: {e.returncode}")
        if e.stdout:
            print(f"Saída: {e.stdout}")
        if e.stderr:
            print(f"Erro: {e.stderr}")
        return False

def main():
    """Função principal para configurar o ambiente de testes."""
    print("🚀 Configurando ambiente de testes para o Otimizador de Currículos com IA")
    print("=" * 70)
    
    # Verifica se estamos no diretório correto
    if not os.path.exists("pyproject.toml"):
        print("❌ Erro: Execute este script no diretório backend/")
        sys.exit(1)
    
    # 1. Instalar dependências
    print("\n📦 Passo 1: Instalando dependências...")
    if not run_command("uv sync", "Instalando dependências com UV"):
        print("❌ Falha ao instalar dependências. Verifique se o UV está instalado.")
        sys.exit(1)
    
    # 2. Instalar modelo spaCy
    print("\n🧠 Passo 2: Instalando modelo spaCy...")
    if not run_command("python -m spacy download pt_core_news_sm", "Instalando modelo spaCy pt_core_news_sm"):
        print("❌ Falha ao instalar modelo spaCy.")
        print("💡 Alternativa: Execute manualmente: python -m spacy download pt_core_news_sm")
    
    # 3. Verificar instalação
    print("\n🔍 Passo 3: Verificando instalação...")
    try:
        import spacy
        nlp = spacy.load("pt_core_news_sm")
        print("✅ Modelo spaCy carregado com sucesso!")
        print(f"📊 Informações do modelo: {nlp.meta['name']} v{nlp.meta['version']}")
    except Exception as e:
        print(f"❌ Erro ao carregar modelo spaCy: {e}")
        print("💡 O modelo pode não ter sido instalado corretamente.")
    
    # 4. Executar testes básicos
    print("\n🧪 Passo 4: Executando testes básicos...")
    if run_command("python test_analysis.py", "Executando testes básicos de análise"):
        print("✅ Testes básicos executados com sucesso!")
    else:
        print("❌ Alguns testes falharam. Verifique as dependências.")
    
    # 5. Executar pytest
    print("\n🧪 Passo 5: Executando pytest...")
    if run_command("uv run pytest tests/ -v", "Executando pytest"):
        print("✅ Todos os testes passaram!")
    else:
        print("❌ Alguns testes falharam. Verifique os logs acima.")
    
    print("\n🎉 Configuração do ambiente de testes concluída!")
    print("\n📚 Comandos úteis:")
    print("   • Executar todos os testes: uv run pytest tests/ -v")
    print("   • Executar testes específicos: uv run pytest tests/unit/test_analysis.py -v")
    print("   • Executar com coverage: uv run pytest tests/ --cov=app --cov-report=html")
    print("   • Executar testes de análise: python test_analysis.py")
    print("\n🚀 Para iniciar a API: uv run uvicorn main:app --reload")

if __name__ == "__main__":
    main()
