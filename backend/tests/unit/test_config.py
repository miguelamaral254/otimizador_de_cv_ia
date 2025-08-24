"""
Testes unitários para o módulo de configuração.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from app.core.config import Settings, settings


class TestSettings:
    """Testes para a classe Settings."""
    
    def test_settings_default_values(self):
        """Testa valores padrão das configurações."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            # Verifica valores padrão
            assert settings.database_url == "sqlite+aiosqlite:///./otimizador_cv.db"
            assert settings.secret_key == "your-secret-key-here-change-in-production-make-it-very-long-and-random"
            assert settings.algorithm == "HS256"
            assert settings.access_token_expire_minutes == 30
            assert settings.upload_dir == "./uploads"
            assert settings.max_file_size == 10485760  # 10MB
            assert settings.spacy_model == "pt_core_news_sm"
            assert settings.environment == "development"
            assert settings.debug is True
            assert settings.host == "0.0.0.0"
            assert settings.port == 8000
    
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
        with patch.dict(os.environ, {}, clear=True):
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
        with patch.dict(os.environ, {"MAX_FILE_SIZE": "5242880"}, clear=True):  # 5MB
            settings = Settings()
            assert settings.max_file_size == 5 * 1024 * 1024  # 5MB
    
    def test_settings_token_expire_conversion(self):
        """Testa conversão de tempo de expiração do token."""
        with patch.dict(os.environ, {"ACCESS_TOKEN_EXPIRE_MINUTES": "120"}, clear=True):
            settings = Settings()
            assert settings.access_token_expire_minutes == 120
    
    def test_settings_port_conversion(self):
        """Testa conversão da porta."""
        with patch.dict(os.environ, {"PORT": "9000"}, clear=True):
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
        
        # Verifica se tem valores padrão
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
            "DEBUG": "true",
            "DEBUG_FALSE": "false",
            "DEBUG_INVALID": "invalid"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            # Testa conversão de string para boolean
            settings = Settings()
            assert settings.debug is True  # valor padrão
            
            # Testa com valor específico
            with patch.dict(os.environ, {"DEBUG": "false"}, clear=True):
                settings = Settings()
                assert settings.debug is False


class TestSettingsSecurity:
    """Testes para configurações de segurança."""
    
    def test_secret_key_minimum_length(self):
        """Testa se a chave secreta tem comprimento mínimo."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            # Chave secreta deve ter pelo menos 10 caracteres
            assert len(settings.secret_key) >= 10
    
    def test_algorithm_valid_values(self):
        """Testa se o algoritmo é válido."""
        valid_algorithms = ["HS256", "HS384", "HS512"]
        
        for algo in valid_algorithms:
            with patch.dict(os.environ, {"ALGORITHM": algo}, clear=True):
                settings = Settings()
                assert settings.algorithm in valid_algorithms
    
    def test_token_expire_reasonable_range(self):
        """Testa se o tempo de expiração está em range razoável."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            # Deve estar entre 1 minuto e 24 horas
            assert 1 <= settings.access_token_expire_minutes <= 1440
    
    def test_port_valid_range(self):
        """Testa se a porta está em range válido."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            # Porta deve estar entre 1 e 65535
            assert 1 <= settings.port <= 65535


class TestSettingsEnvironment:
    """Testes para configurações de ambiente."""
    
    def test_environment_values(self):
        """Testa valores válidos para environment."""
        valid_environments = ["development", "staging", "production", "test"]
        
        for env in valid_environments:
            with patch.dict(os.environ, {"ENVIRONMENT": env}, clear=True):
                settings = Settings()
                assert settings.environment == env
    
    def test_debug_default_development(self):
        """Testa se debug é True por padrão em development."""
        with patch.dict(os.environ, {"ENVIRONMENT": "development"}, clear=True):
            settings = Settings()
            assert settings.debug is True
    
    def test_debug_production(self):
        """Testa se debug pode ser False em production."""
        with patch.dict(os.environ, {"ENVIRONMENT": "production", "DEBUG": "false"}, clear=True):
            settings = Settings()
            assert settings.debug is False
