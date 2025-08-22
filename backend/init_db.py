#!/usr/bin/env python3
"""
Script para inicialização do banco de dados.
Execute este script para criar as tabelas e dados iniciais.
"""

import asyncio
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from app.core.database import create_tables, engine
from app.core.config import settings
from app.models.user import User
from app.models.curriculum import Curriculum, CurriculumVersion, CurriculumAnalysis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from passlib.context import CryptContext

# Configuração para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_initial_data():
    """Cria dados iniciais para teste."""
    async with AsyncSessionLocal() as db:
        try:
            # Verifica se já existe um usuário admin
            from sqlalchemy import select
            result = await db.execute(select(User).where(User.username == "admin"))
            admin_user = result.scalar_one_or_none()
            
            if not admin_user:
                # Cria usuário admin
                hashed_password = pwd_context.hash("admin123")
                admin_user = User(
                    email="admin@exemplo.com",
                    username="admin",
                    hashed_password=hashed_password
                )
                db.add(admin_user)
                await db.commit()
                await db.refresh(admin_user)
                print("✅ Usuário admin criado com sucesso!")
                print(f"   Username: admin")
                print(f"   Senha: admin123")
            else:
                print("ℹ️  Usuário admin já existe")
                
        except Exception as e:
            print(f"❌ Erro ao criar dados iniciais: {e}")
            await db.rollback()


async def main():
    """Função principal."""
    print("🚀 Inicializando banco de dados...")
    
    try:
        # Cria as tabelas
        await create_tables()
        print("✅ Tabelas criadas com sucesso!")
        
        # Cria dados iniciais
        await create_initial_data()
        
        print("🎉 Banco de dados inicializado com sucesso!")
        print(f"📁 Arquivo do banco: {settings.database_url}")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


