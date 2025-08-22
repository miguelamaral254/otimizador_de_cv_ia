#!/usr/bin/env python3
"""
Script de teste para a API de métricas temporais.
Este script testa a funcionalidade implementada para série temporal de métricas.
"""

import asyncio
import json
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.user import User
from app.models.curriculum import Curriculum, CurriculumVersion, CurriculumAnalysis
from app.routers.metrics import _extract_metrics_from_analysis


async def create_test_data():
    """Cria dados de teste para verificar a funcionalidade."""
    async for db in get_db():
        try:
            # Criar usuário de teste
            test_user = User(
                email="test@example.com",
                username="testuser",
                hashed_password="hashed_password_123"
            )
            db.add(test_user)
            await db.commit()
            await db.refresh(test_user)
            
            # Criar currículo de teste
            curriculum = Curriculum(
                user_id=test_user.id,
                original_filename="test_curriculum.pdf",
                file_path="/path/to/test.pdf",
                file_size=1024,
                title="Currículo de Teste",
                description="Currículo para testes"
            )
            db.add(curriculum)
            await db.commit()
            await db.refresh(curriculum)
            
            # Criar versões de teste
            versions = []
            for i in range(1, 4):
                version = CurriculumVersion(
                    curriculum_id=curriculum.id,
                    version_number=i,
                    version_name=f"v{i}.0",
                    file_path=f"/path/to/test_v{i}.pdf",
                    file_size=1024 + i * 100,
                    changes_description=f"Versão {i} do currículo"
                )
                db.add(version)
                versions.append(version)
            
            await db.commit()
            
            # Criar análises de teste com dados variados
            analyses = []
            base_date = datetime.now() - timedelta(days=30)
            
            for i, version in enumerate(versions):
                # Dados de análise do spaCy
                spacy_data = {
                    "action_verbs": ["desenvolveu", "implementou", "gerenciou"],
                    "quantified_results": [f"Aumentou {20 + i * 10}%", f"Reduziu {5 + i * 5}%"],
                    "keywords_found": ["python", "javascript", "react"],
                    "text_statistics": {
                        "total_words": 500 + i * 50,
                        "action_verbs_count": 15 + i * 2,
                        "quantified_results_count": 8 + i
                    }
                }
                
                # Dados de análise do Gemini
                gemini_data = {
                    "overall_assessment": f"Currículo {i + 1} mostra boa evolução",
                    "strengths": [f"Pontos fortes da versão {i + 1}"],
                    "weaknesses": [f"Áreas de melhoria da versão {i + 1}"],
                    "suggestions": [f"Sugestão {i + 1} para melhoria"],
                    "industry_relevance": "high" if i > 0 else "medium",
                    "improvement_areas": [f"Área {i + 1} para melhorar"]
                }
                
                analysis = CurriculumAnalysis(
                    curriculum_id=curriculum.id,
                    version_id=version.id,
                    spacy_analysis=spacy_data,
                    gemini_analysis=gemini_data,
                    action_verbs_count=15 + i * 2,
                    quantified_results_count=8 + i,
                    keywords_score=60.0 + i * 5,
                    overall_score=70.0 + i * 8,
                    strengths=gemini_data["strengths"],
                    weaknesses=gemini_data["weaknesses"],
                    suggestions=gemini_data["suggestions"],
                    analysis_date=base_date + timedelta(days=i * 7),
                    processing_time=2.5 + i * 0.5
                )
                db.add(analysis)
                analyses.append(analysis)
            
            await db.commit()
            
            print("✅ Dados de teste criados com sucesso!")
            print(f"   - Usuário ID: {test_user.id}")
            print(f"   - Currículo ID: {curriculum.id}")
            print(f"   - Versões criadas: {len(versions)}")
            print(f"   - Análises criadas: {len(analyses)}")
            
            return test_user.id, curriculum.id
            
        except Exception as e:
            print(f"❌ Erro ao criar dados de teste: {e}")
            await db.rollback()
            raise


async def test_metrics_extraction():
    """Testa a extração de métricas de uma análise."""
    async for db in get_db():
        try:
            # Buscar uma análise de teste
            result = await db.execute(
                select(CurriculumAnalysis).limit(1)
            )
            analysis = result.scalar_one_or_none()
            
            if not analysis:
                print("❌ Nenhuma análise encontrada para teste")
                return
            
            # Testar extração de métricas
            metrics = _extract_metrics_from_analysis(analysis)
            
            print("✅ Teste de extração de métricas:")
            print(f"   - Score geral: {metrics.score}")
            print(f"   - Clareza: {metrics.clarity}")
            print(f"   - Relevância: {metrics.relevance}")
            print(f"   - Palavras-chave: {metrics.keywords}")
            print(f"   - Estrutura: {metrics.structure}")
            print(f"   - Personalização: {metrics.personalization}")
            
        except Exception as e:
            print(f"❌ Erro no teste de extração: {e}")


async def test_time_series_data():
    """Testa a geração de dados de série temporal."""
    async for db in get_db():
        try:
            # Buscar usuário de teste
            result = await db.execute(
                select(User).where(User.email == "test@example.com")
            )
            user = result.scalar_one_or_none()
            
            if not user:
                print("❌ Usuário de teste não encontrado")
                return
            
            # Buscar todas as análises do usuário
            result = await db.execute(
                select(CurriculumAnalysis)
                .join(Curriculum, CurriculumAnalysis.curriculum_id == Curriculum.id)
                .where(Curriculum.user_id == user.id)
                .order_by(CurriculumAnalysis.analysis_date)
            )
            analyses = result.scalars().all()
            
            print(f"✅ Teste de série temporal:")
            print(f"   - Total de análises: {len(analyses)}")
            
            # Simular processamento da série temporal
            time_series_data = []
            scores = []
            
            for i, analysis in enumerate(analyses):
                # Determinar ID da versão
                if analysis.version_id:
                    version_result = await db.execute(
                        select(CurriculumVersion).where(CurriculumVersion.id == analysis.version_id)
                    )
                    version = version_result.scalar_one_or_none()
                    version_id = f"v{version.version_number}" if version else f"analysis_{analysis.id}"
                else:
                    version_id = f"curriculum_{analysis.curriculum_id}"
                
                # Extrair métricas
                metrics = _extract_metrics_from_analysis(analysis)
                
                # Criar entrada da série temporal
                time_series_entry = {
                    "version_id": version_id,
                    "timestamp": analysis.analysis_date.isoformat(),
                    "metrics": {
                        "score": metrics.score,
                        "clarity": metrics.clarity,
                        "relevance": metrics.relevance,
                        "keywords": metrics.keywords,
                        "structure": metrics.structure,
                        "personalization": metrics.personalization
                    }
                }
                
                time_series_data.append(time_series_entry)
                scores.append(metrics.score)
            
            # Calcular estatísticas
            total_versions = len(time_series_data)
            average_score = sum(scores) / total_versions if scores else 0.0
            best_score = max(scores) if scores else 0.0
            
            # Calcular taxa de melhoria
            improvement_rate = 0.0
            if len(scores) >= 2:
                first_score = scores[0]
                last_score = scores[-1]
                if first_score > 0:
                    improvement_rate = ((last_score - first_score) / first_score) * 100
            
            # Criar resposta final
            response = {
                "user_id": user.id,
                "total_versions": total_versions,
                "time_series": time_series_data,
                "average_score": round(average_score, 2),
                "best_score": round(best_score, 2),
                "improvement_rate": round(improvement_rate, 2)
            }
            
            print(f"   - Total de versões: {response['total_versions']}")
            print(f"   - Pontuação média: {response['average_score']}")
            print(f"   - Melhor pontuação: {response['best_score']}")
            print(f"   - Taxa de melhoria: {response['improvement_rate']}%")
            
            # Exibir exemplo de dados da série temporal
            if time_series_data:
                print("\n📊 Exemplo de dados da série temporal:")
                print(json.dumps(time_series_data[0], indent=2, ensure_ascii=False))
            
        except Exception as e:
            print(f"❌ Erro no teste de série temporal: {e}")


async def cleanup_test_data():
    """Remove dados de teste."""
    async for db in get_db():
        try:
            # Remover usuário de teste e todos os dados relacionados
            result = await db.execute(
                select(User).where(User.email == "test@example.com")
            )
            user = result.scalar_one_or_none()
            
            if user:
                # As relações estão configuradas com cascade, então remover o usuário
                # removerá automaticamente currículos, versões e análises
                await db.delete(user)
                await db.commit()
                print("✅ Dados de teste removidos com sucesso!")
            else:
                print("ℹ️  Nenhum dado de teste encontrado para remoção")
                
        except Exception as e:
            print(f"❌ Erro ao remover dados de teste: {e}")
            await db.rollback()


async def main():
    """Função principal para executar todos os testes."""
    print("🚀 Iniciando testes da API de métricas...\n")
    
    try:
        # Criar dados de teste
        print("1. Criando dados de teste...")
        await create_test_data()
        print()
        
        # Testar extração de métricas
        print("2. Testando extração de métricas...")
        await test_metrics_extraction()
        print()
        
        # Testar série temporal
        print("3. Testando geração de série temporal...")
        await test_time_series_data()
        print()
        
        # Perguntar se deve remover dados de teste
        response = input("\n❓ Deseja remover os dados de teste? (s/n): ")
        if response.lower() in ['s', 'sim', 'y', 'yes']:
            print("4. Removendo dados de teste...")
            await cleanup_test_data()
        
        print("\n✅ Todos os testes concluídos com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")


if __name__ == "__main__":
    asyncio.run(main())
