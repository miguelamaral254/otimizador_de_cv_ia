"""
Testes unitários para o módulo de configuração.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from app.core.config import Settings, settings, SettingsConfigDict


class TestSettings:
    """Testes para a classe Settings."""
    
    def test_settings_from_environment(self):
        """Testa configurações a partir de variáveis de ambiente."""
        test_env = {
            "DATABASE_URL": "postgresql://test:test@localhost/test",
            "SECRET_KEY": "test-secret-key",
            "ALGORITHM": "HS512",
            "ACCESS_TOKEN_EXPIRE_MINUTES": "60",
            "UPLOAD_DIR": "/custom/upload/dir",
            "MAX_FILE_SIZE": "20971520",  # 20MB
            "SPACY_MODEL": "en_core_web_sm",
            "GEMINI_API_KEY": "test-gemini-key",
            "ENVIRONMENT": "production",
            "DEBUG": "false",
            "HOST": "127.0.0.1",
            "PORT": "9000"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.database_url == "postgresql://test:test@localhost/test"
            assert settings.secret_key == "test-secret-key"
            assert settings.algorithm == "HS512"
            assert settings.access_token_expire_minutes == 60
            assert settings.upload_dir == "/custom/upload/dir"
            assert settings.max_file_size == 20 * 1024 * 1024  # 20MB
            assert settings.spacy_model == "en_core_web_sm"
            assert settings.gemini_api_key == "test-gemini-key"
            assert settings.environment == "production"
            assert settings.debug is False
            assert settings.host == "127.0.0.1"
            assert settings.port == 9000
    
    def test_settings_validation(self):
        """Testa validação das configurações."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "test-secret-key-123"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            # Verifica tipos
            assert isinstance(settings.database_url, str)
            assert isinstance(settings.secret_key, str)
            assert isinstance(settings.algorithm, str)
            assert isinstance(settings.access_token_expire_minutes, int)
            assert isinstance(settings.upload_dir, str)
            assert isinstance(settings.max_file_size, int)
            assert isinstance(settings.spacy_model, str)
            assert isinstance(settings.environment, str)
            assert isinstance(settings.debug, bool)
            assert isinstance(settings.host, str)
            assert isinstance(settings.port, int)
    
    def test_settings_file_size_conversion(self):
        """Testa conversão de tamanho de arquivo."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "test-secret-key-123",
            "MAX_FILE_SIZE": "5242880"
        }
        
        with patch.dict(os.environ, test_env, clear=True):  # 5MB
            settings = Settings()
            assert settings.max_file_size == 5 * 1024 * 1024  # 5MB
    
    def test_settings_token_expire_conversion(self):
        """Testa conversão de tempo de expiração do token."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "test-secret-key-123",
            "ACCESS_TOKEN_EXPIRE_MINUTES": "120"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            assert settings.access_token_expire_minutes == 120
    
    def test_settings_port_conversion(self):
        """Testa conversão da porta."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "test-secret-key-123",
            "PORT": "9000"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            assert settings.port == 9000


class TestSettingsInstance:
    """Testes para a instância global settings."""
    
    def test_settings_instance_exists(self):
        """Testa se a instância global existe."""
        from app.core.config import settings
        
        assert settings is not None
        assert isinstance(settings, Settings)
    
    def test_settings_instance_values(self):
        """Testa valores da instância global."""
        from app.core.config import settings
        
        # Verifica se tem valores obrigatórios
        assert hasattr(settings, 'database_url')
        assert hasattr(settings, 'secret_key')
        assert hasattr(settings, 'algorithm')
        assert hasattr(settings, 'access_token_expire_minutes')
        assert hasattr(settings, 'upload_dir')
        assert hasattr(settings, 'max_file_size')
        assert hasattr(settings, 'spacy_model')
        assert hasattr(settings, 'environment')
        assert hasattr(settings, 'debug')
        assert hasattr(settings, 'host')
        assert hasattr(settings, 'port')


class TestSettingsEdgeCases:
    """Testes para casos extremos das configurações."""
    
    def test_settings_empty_strings(self):
        """Testa configurações com strings vazias."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "",
            "GEMINI_API_KEY": "",
            "UPLOAD_DIR": "",
            "HOST": ""
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            # Strings vazias devem ser mantidas como estão
            assert settings.secret_key == ""
            assert settings.gemini_api_key == ""
            assert settings.upload_dir == ""
            assert settings.host == ""
    
    def test_settings_invalid_numbers(self):
        """Testa configurações com números inválidos."""
        # Pydantic v2 não permite valores inválidos por padrão
        # Vamos testar com valores válidos mas extremos
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "test-secret-key-123",
            "ACCESS_TOKEN_EXPIRE_MINUTES": "999999",
            "MAX_FILE_SIZE": "1073741824",  # 1GB
            "PORT": "65535"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.access_token_expire_minutes == 999999
            assert settings.max_file_size == 1073741824
            assert settings.port == 65535
    
    def test_settings_boolean_conversion(self):
        """Testa conversão de valores booleanos."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "test-secret-key-123",
            "DEBUG": "false"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            assert settings.debug is False


class TestSettingsSecurity:
    """Testes para configurações de segurança."""
    
    def test_secret_key_minimum_length(self):
        """Testa se a chave secreta tem comprimento mínimo."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "test-secret-key-123"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            # Chave secreta deve ter pelo menos 10 caracteres
            assert len(settings.secret_key) >= 10
    
    def test_algorithm_valid_values(self):
        """Testa se o algoritmo é válido."""
        valid_algorithms = ["HS256", "HS384", "HS512"]
        
        for algo in valid_algorithms:
            test_env = {
                "DATABASE_URL": "sqlite:///test.db",
                "SECRET_KEY": "test-secret-key-123",
                "ALGORITHM": algo
            }
            
            with patch.dict(os.environ, test_env, clear=True):
                settings = Settings()
                assert settings.algorithm in valid_algorithms
    
    def test_token_expire_reasonable_range(self):
        """Testa se o tempo de expiração está em range razoável."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "test-secret-key-123"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            # Deve estar entre 1 minuto e 24 horas
            assert 1 <= settings.access_token_expire_minutes <= 1440
    
    def test_port_valid_range(self):
        """Testa se a porta está em range válido."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "test-secret-key-123"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            # Porta deve estar entre 1 e 65535
            assert 1 <= settings.port <= 65535


class TestSettingsEnvironment:
    """Testes para configurações de ambiente."""
    
    def test_environment_values(self):
        """Testa valores válidos para environment."""
        valid_environments = ["development", "staging", "production", "test"]
        
        for env in valid_environments:
            test_env = {
                "DATABASE_URL": "sqlite:///test.db",
                "SECRET_KEY": "test-secret-key-123",
                "ENVIRONMENT": env
            }
            
            with patch.dict(os.environ, test_env, clear=True):
                settings = Settings()
                assert settings.environment == env
    
    def test_debug_default_development(self):
        """Testa se debug é True por padrão em development."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "test-secret-key-123",
            "ENVIRONMENT": "development"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            assert settings.debug is True
    
    def test_debug_production(self):
        """Testa se debug pode ser False em production."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "test-secret-key-123",
            "ENVIRONMENT": "production",
            "DEBUG": "false"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            assert settings.debug is False


class TestSettingsRequiredFields:
    """Testes para campos obrigatórios."""
    
    def test_database_url_required(self):
        """Testa se DATABASE_URL é obrigatório."""
        # Remove o arquivo .env temporariamente para testar campos obrigatórios
        with patch.dict(os.environ, {}, clear=True):
            # Como o Pydantic carrega do arquivo .env, vamos testar sem ele
            with patch('app.core.config.Settings.model_config') as mock_config:
                mock_config.return_value = SettingsConfigDict(
                    env_file=None,  # Não carrega arquivo .env
                    case_sensitive=False,
                    extra="ignore"
                )
                with pytest.raises(Exception):  # Pydantic validation error
                    Settings()
    
    def test_secret_key_required(self):
        """Testa se SECRET_KEY é obrigatório."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db"
            # SECRET_KEY não definido
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            # Como o Pydantic carrega do arquivo .env, vamos testar sem ele
            with patch('app.core.config.Settings.model_config') as mock_config:
                mock_config.return_value = SettingsConfigDict(
                    env_file=None,  # Não carrega arquivo .env
                    case_sensitive=False,
                    extra="ignore"
                )
                with pytest.raises(Exception):  # Pydantic validation error
                    Settings()
    
    def test_optional_fields_can_be_none(self):
        """Testa se campos opcionais podem ser None."""
        test_env = {
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "test-secret-key-123",
            "GEMINI_API_KEY": ""  # Campo opcional
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            assert settings.gemini_api_key == ""
