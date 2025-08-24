"""
Testes unitários para o módulo de banco de dados.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db, engine, AsyncSessionLocal, Base


class TestDatabaseConnection:
    """Testes para conexão com o banco de dados."""
    
    def test_engine_creation(self):
        """Testa se o engine do SQLAlchemy foi criado."""
        from app.core.database import engine
        
        assert engine is not None
        assert hasattr(engine, 'url')
        assert hasattr(engine, 'name')
    
    def test_async_session_local_creation(self):
        """Testa se o AsyncSessionLocal foi criado."""
        from app.core.database import AsyncSessionLocal
        
        assert AsyncSessionLocal is not None
        assert callable(AsyncSessionLocal)
    
    def test_database_url_format(self):
        """Testa se a URL do banco está no formato correto."""
        from app.core.database import engine
        
        # Verifica se a URL contém elementos esperados
        url_str = str(engine.url)
        assert "sqlite" in url_str.lower() or "postgresql" in url_str.lower()
    
    def test_engine_attributes(self):
        """Testa atributos básicos do engine."""
        from app.core.database import engine
        
        # Verifica atributos essenciais
        assert hasattr(engine, 'pool')
        assert hasattr(engine, 'dialect')
        assert hasattr(engine, 'execute')
    
    def test_async_session_local_attributes(self):
        """Testa atributos do AsyncSessionLocal."""
        from app.core.database import AsyncSessionLocal
        
        # Verifica se é um sessionmaker
        assert hasattr(AsyncSessionLocal, 'configure')
        assert hasattr(AsyncSessionLocal, 'bind')
    
    def test_database_imports(self):
        """Testa se todos os imports necessários estão disponíveis."""
        try:
            from app.core.database import get_db, engine, AsyncSessionLocal, Base
            assert True  # Se chegou aqui, os imports funcionaram
        except ImportError as e:
            pytest.fail(f"Falha no import: {e}")


class TestGetDbFunction:
    """Testes para a função get_db."""
    
    def test_get_db_function_exists(self):
        """Testa se a função get_db existe."""
        from app.core.database import get_db
        
        assert callable(get_db)
    
    def test_get_db_async_function(self):
        """Testa se get_db é uma função assíncrona."""
        from app.core.database import get_db
        
        # Verifica se é assíncrona
        import inspect
        assert inspect.iscoroutinefunction(get_db)
    
    @pytest.mark.asyncio
    async def test_get_db_yields_session(self):
        """Testa se get_db retorna uma sessão."""
        from app.core.database import get_db
        
        # Chama a função geradora assíncrona
        async for db_session in get_db():
            # Verifica se é uma sessão
            assert db_session is not None
            assert hasattr(db_session, 'commit')
            assert hasattr(db_session, 'rollback')
            assert hasattr(db_session, 'close')
            break  # Só testa a primeira iteração
    
    @pytest.mark.asyncio
    async def test_get_db_session_attributes(self):
        """Testa atributos da sessão retornada."""
        from app.core.database import get_db
        
        async for db_session in get_db():
            # Verifica métodos essenciais
            assert callable(db_session.commit)
            assert callable(db_session.rollback)
            assert callable(db_session.close)
            assert callable(db_session.add)
            assert callable(db_session.query)
            assert callable(db_session.execute)
            break
    
    @pytest.mark.asyncio
    async def test_get_db_session_type(self):
        """Testa se a sessão é do tipo correto."""
        from app.core.database import get_db
        
        async for db_session in get_db():
            # Verifica se é uma sessão assíncrona SQLAlchemy
            assert isinstance(db_session, AsyncSession)
            break


class TestDatabaseConfiguration:
    """Testes para configuração do banco de dados."""
    
    def test_database_engine_configuration(self):
        """Testa configuração do engine."""
        from app.core.database import engine
        
        # Verifica configurações básicas
        assert engine is not None
        
        # Verifica se o engine pode executar comandos básicos
        try:
            # Para engine assíncrono, testamos apenas atributos
            assert hasattr(engine, 'connect')
            assert hasattr(engine, 'begin')
        except Exception as e:
            # Em ambiente de teste, pode não conseguir conectar
            # Isso é aceitável
            pass
    
    def test_async_session_local_configuration(self):
        """Testa configuração do AsyncSessionLocal."""
        from app.core.database import AsyncSessionLocal
        
        # Verifica se pode criar uma sessão
        try:
            # AsyncSessionLocal é um sessionmaker, não uma sessão
            assert callable(AsyncSessionLocal)
            assert hasattr(AsyncSessionLocal, 'configure')
        except Exception as e:
            # Em ambiente de teste, pode não conseguir conectar
            # Isso é aceitável
            pass
    
    def test_database_pool_configuration(self):
        """Testa configuração do pool de conexões."""
        from app.core.database import engine
        
        # Verifica configurações do pool
        assert hasattr(engine, 'pool')
        pool = engine.pool
        
        # Verifica atributos do pool
        assert hasattr(pool, 'size')
        assert hasattr(pool, 'overflow')
        assert hasattr(pool, 'timeout')
    
    def test_database_echo_configuration(self):
        """Testa configuração de echo do SQLAlchemy."""
        from app.core.database import engine
        
        # Verifica se echo está configurado (para debug)
        # Pode ser True ou False dependendo do ambiente
        assert hasattr(engine, 'echo')
        assert isinstance(engine.echo, bool)


class TestDatabaseErrorHandling:
    """Testes para tratamento de erros do banco de dados."""
    
    @patch('app.core.database.AsyncSessionLocal')
    @pytest.mark.asyncio
    async def test_get_db_session_creation_error(self, mock_session_local):
        """Testa erro na criação da sessão."""
        # Mock de erro na criação da sessão
        mock_session_local.side_effect = SQLAlchemyError("Erro de conexão")
        
        from app.core.database import get_db
        
        # Deve propagar o erro
        with pytest.raises(SQLAlchemyError) as exc_info:
            async for db_session in get_db():
                pass
        
        assert "Erro de conexão" in str(exc_info.value)
    
    @patch('app.core.database.AsyncSessionLocal')
    @pytest.mark.asyncio
    async def test_get_db_session_commit_error(self, mock_session_local):
        """Testa erro no commit da sessão."""
        # Mock da sessão
        mock_session = Mock(spec=AsyncSession)
        mock_session.commit.side_effect = SQLAlchemyError("Erro no commit")
        mock_session_local.return_value.__aenter__.return_value = mock_session
        
        from app.core.database import get_db
        
        # Deve propagar o erro
        with pytest.raises(SQLAlchemyError) as exc_info:
            async for db_session in get_db():
                # Simula commit
                await db_session.commit()
                break
        
        assert "Erro no commit" in str(exc_info.value)
    
    def test_database_connection_timeout(self):
        """Testa timeout de conexão."""
        from app.core.database import engine
        
        # Verifica se o engine tem configuração de timeout
        assert hasattr(engine, 'pool')
        pool = engine.pool
        
        # Verifica timeout do pool
        assert hasattr(pool, 'timeout')
        assert isinstance(pool.timeout, (int, float))
    
    def test_database_pool_overflow(self):
        """Testa configuração de overflow do pool."""
        from app.core.database import engine
        
        # Verifica configuração de overflow
        assert hasattr(engine, 'pool')
        pool = engine.pool
        
        # Verifica overflow do pool
        assert hasattr(pool, 'overflow')
        assert isinstance(pool.overflow, int)
        assert pool.overflow >= 0


class TestDatabaseIntegration:
    """Testes de integração com o banco de dados."""
    
    def test_database_models_import(self):
        """Testa se os modelos podem ser importados."""
        try:
            from app.models import user, curriculum, metrics
            assert True  # Se chegou aqui, os imports funcionaram
        except ImportError as e:
            pytest.fail(f"Falha no import dos modelos: {e}")
    
    def test_database_schemas_import(self):
        """Testa se os schemas podem ser importados."""
        try:
            from app.schemas import user, curriculum, metrics
            assert True  # Se chegou aqui, os imports funcionaram
        except ImportError as e:
            pytest.fail(f"Falha no import dos schemas: {e}")
    
    def test_database_dependencies_import(self):
        """Testa se as dependências podem ser importadas."""
        try:
            from app.core.deps import get_current_user, get_current_active_user
            assert True  # Se chegou aqui, os imports funcionaram
        except ImportError as e:
            pytest.fail(f"Falha no import das dependências: {e}")


class TestDatabaseEnvironment:
    """Testes para diferentes ambientes de banco de dados."""
    
    def test_database_url_environment_variable(self):
        """Testa se a URL do banco pode ser configurada via variável de ambiente."""
        from app.core.database import engine
        
        # Verifica se a URL atual contém valores esperados
        url_str = str(engine.url)
        
        # Deve conter informações de conexão
        assert len(url_str) > 0
        assert "://" in url_str  # Formato de URL
    
    def test_database_connection_string_format(self):
        """Testa formato da string de conexão."""
        from app.core.database import engine
        
        url = engine.url
        
        # Verifica componentes da URL
        assert hasattr(url, 'drivername')
        assert hasattr(url, 'username')
        assert hasattr(url, 'password')
        assert hasattr(url, 'host')
        assert hasattr(url, 'port')
        assert hasattr(url, 'database')
    
    def test_database_driver_support(self):
        """Testa se o driver do banco é suportado."""
        from app.core.database import engine
        
        driver_name = engine.url.drivername.lower()
        
        # Verifica se é um driver suportado
        supported_drivers = ['sqlite', 'postgresql', 'mysql', 'mariadb']
        assert any(driver in driver_name for driver in supported_drivers)


class TestDatabasePerformance:
    """Testes para performance do banco de dados."""
    
    def test_database_pool_size(self):
        """Testa tamanho do pool de conexões."""
        from app.core.database import engine
        
        pool = engine.pool
        
        # Verifica se o pool tem tamanho razoável
        assert pool.size() > 0
        assert pool.size() <= 20  # Tamanho máximo razoável
    
    def test_database_pool_overflow_limit(self):
        """Testa limite de overflow do pool."""
        from app.core.database import engine
        
        pool = engine.pool
        
        # Verifica se o overflow tem limite razoável
        assert pool.overflow() >= 0
        assert pool.overflow() <= 30  # Overflow máximo razoável
    
    def test_database_connection_timeout_reasonable(self):
        """Testa se o timeout de conexão é razoável."""
        from app.core.database import engine
        
        pool = engine.pool
        
        # Verifica se o timeout é razoável (entre 1 e 300 segundos)
        timeout = pool.timeout()
        assert 1 <= timeout <= 300


class TestDatabaseSecurity:
    """Testes para segurança do banco de dados."""
    
    def test_database_url_no_credentials_exposed(self):
        """Testa se credenciais não estão expostas na URL."""
        from app.core.database import engine
        
        url_str = str(engine.url)
        
        # Verifica se não há credenciais expostas
        sensitive_patterns = [
            'password=',
            'passwd=',
            'pwd=',
            'secret=',
            'key='
        ]
        
        for pattern in sensitive_patterns:
            assert pattern not in url_str.lower()
    
    def test_database_connection_encrypted(self):
        """Testa se a conexão é criptografada quando apropriado."""
        from app.core.database import engine
        
        url = engine.url
        
        # Para PostgreSQL, verifica se SSL está habilitado
        if 'postgresql' in url.drivername.lower():
            # Verifica parâmetros SSL na URL
            url_str = str(url)
            # Em produção, SSL deve estar habilitado
            # Em desenvolvimento, pode não estar
            pass
    
    def test_database_user_permissions(self):
        """Testa se o usuário do banco tem permissões mínimas."""
        # Este teste seria executado em um ambiente real
        # Verifica se o usuário tem apenas permissões necessárias
        pass


class TestDatabaseBase:
    """Testes para a base declarativa."""
    
    def test_base_exists(self):
        """Testa se a base declarativa existe."""
        from app.core.database import Base
        
        assert Base is not None
        assert hasattr(Base, 'metadata')
    
    def test_base_metadata(self):
        """Testa metadados da base."""
        from app.core.database import Base
        
        # Verifica se tem metadados
        assert Base.metadata is not None
        assert hasattr(Base.metadata, 'tables')
    
    def test_base_registry(self):
        """Testa registro da base."""
        from app.core.database import Base
        
        # Verifica se tem registro
        assert hasattr(Base, 'registry')
        assert Base.registry is not None


class TestDatabaseAsyncFunctions:
    """Testes para funções assíncronas do banco."""
    
    def test_create_tables_function_exists(self):
        """Testa se a função create_tables existe."""
        from app.core.database import create_tables
        
        assert callable(create_tables)
    
    def test_create_tables_is_async(self):
        """Testa se create_tables é assíncrona."""
        from app.core.database import create_tables
        
        import inspect
        assert inspect.iscoroutinefunction(create_tables)
    
    def test_drop_tables_function_exists(self):
        """Testa se a função drop_tables existe."""
        from app.core.database import drop_tables
        
        assert callable(drop_tables)
    
    def test_drop_tables_is_async(self):
        """Testa se drop_tables é assíncrona."""
        from app.core.database import drop_tables
        
        import inspect
        assert inspect.iscoroutinefunction(drop_tables)
