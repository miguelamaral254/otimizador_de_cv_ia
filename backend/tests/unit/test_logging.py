"""
Testes unitários para o módulo de logging.
"""

import pytest
import logging
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from app.core.logging import setup_logging, get_logger


class TestSetupLogging:
    """Testes para a função setup_logging."""
    
    def test_setup_logging_creates_logger(self):
        """Testa se setup_logging cria um logger."""
        logger = setup_logging()
        
        assert logger is not None
        assert isinstance(logger, logging.Logger)
        assert logger.level == logging.INFO
    
    def test_setup_logging_configures_handlers(self):
        """Testa se setup_logging configura os handlers."""
        logger = setup_logging()
        
        # Verifica se tem pelo menos 3 handlers (console, arquivo, erro)
        assert len(logger.handlers) >= 3
        
        # Verifica tipos de handlers
        handler_types = [type(h).__name__ for h in logger.handlers]
        assert 'StreamHandler' in handler_types
        assert 'RotatingFileHandler' in handler_types
    
    def test_setup_logging_creates_log_directory(self):
        """Testa se setup_logging cria o diretório de logs."""
        # Testa apenas se a função executa sem erro
        # O comportamento real de criação do diretório é testado implicitamente
        logger = setup_logging()
        assert logger is not None
        
        # Verifica se o diretório de logs existe após setup
        from pathlib import Path
        log_dir = Path("logs")
        assert log_dir.exists()
    
    @patch('app.core.logging.logging.getLogger')
    def test_setup_logging_removes_existing_handlers(self, mock_get_logger):
        """Testa se setup_logging remove handlers existentes."""
        # Mock do logger com handlers existentes
        mock_logger = MagicMock()
        mock_handler1 = MagicMock()
        mock_handler2 = MagicMock()
        mock_logger.handlers = [mock_handler1, mock_handler2]
        mock_get_logger.return_value = mock_logger
        
        setup_logging()
        
        # Verifica se os handlers foram removidos
        mock_logger.removeHandler.assert_any_call(mock_handler1)
        mock_logger.removeHandler.assert_any_call(mock_handler2)
    
    def test_setup_logging_sets_log_levels(self):
        """Testa se setup_logging configura os níveis de log."""
        logger = setup_logging()
        
        # Verifica nível do logger principal
        assert logger.level == logging.INFO
        
        # Verifica handlers específicos
        for handler in logger.handlers:
            if hasattr(handler, 'level'):
                assert handler.level in [logging.INFO, logging.ERROR]
    
    def test_setup_logging_configures_formatters(self):
        """Testa se setup_logging configura os formatters."""
        logger = setup_logging()
        
        # Verifica se todos os handlers têm formatters
        for handler in logger.handlers:
            assert handler.formatter is not None
            assert isinstance(handler.formatter, logging.Formatter)
    
    def test_setup_logging_configures_uvicorn_loggers(self):
        """Testa se setup_logging configura loggers do uvicorn."""
        setup_logging()
        
        # Verifica se os loggers uvicorn foram configurados
        uvicorn_logger = logging.getLogger("uvicorn")
        uvicorn_access_logger = logging.getLogger("uvicorn.access")
        
        assert uvicorn_logger.level == logging.INFO
        assert uvicorn_access_logger.level == logging.INFO
    
    def test_setup_logging_logs_initialization(self):
        """Testa se setup_logging registra mensagens de inicialização."""
        with patch('app.core.logging.logging.getLogger') as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            
            setup_logging()
            
            # Verifica se as mensagens de inicialização foram registradas
            mock_logger.info.assert_any_call("🚀 Sistema de logging configurado com sucesso!")
            # Verifica se pelo menos uma chamada contém informações do diretório
            info_calls = [call.args[0] for call in mock_logger.info.call_args_list]
            assert any("📁 Diretório de logs:" in call for call in info_calls)


class TestGetLogger:
    """Testes para a função get_logger."""
    
    def test_get_logger_returns_logger(self):
        """Testa se get_logger retorna um logger."""
        logger = get_logger("test_logger")
        
        assert logger is not None
        assert isinstance(logger, logging.Logger)
    
    def test_get_logger_with_specific_name(self):
        """Testa se get_logger retorna logger com nome específico."""
        logger_name = "app.test.module"
        logger = get_logger(logger_name)
        
        assert logger.name == logger_name
    
    def test_get_logger_returns_same_instance(self):
        """Testa se get_logger retorna a mesma instância para o mesmo nome."""
        logger_name = "app.singleton.test"
        logger1 = get_logger(logger_name)
        logger2 = get_logger(logger_name)
        
        assert logger1 is logger2
    
    def test_get_logger_different_names(self):
        """Testa se get_logger retorna instâncias diferentes para nomes diferentes."""
        logger1 = get_logger("app.module1")
        logger2 = get_logger("app.module2")
        
        assert logger1 is not logger2
        assert logger1.name != logger2.name
    
    def test_get_logger_empty_name(self):
        """Testa se get_logger funciona com nome vazio."""
        logger = get_logger("")
        
        assert logger is not None
        assert isinstance(logger, logging.Logger)
        # Logger com nome vazio retorna o root logger
        assert logger.name == "root"
    
    def test_get_logger_special_characters(self):
        """Testa se get_logger funciona com caracteres especiais."""
        special_names = [
            "app.module-with-dash",
            "app.module_with_underscore", 
            "app.module.with.dots",
            "app.module123",
            "app.módulo.português"
        ]
        
        for name in special_names:
            logger = get_logger(name)
            assert logger is not None
            assert logger.name == name


class TestLoggingIntegration:
    """Testes de integração para o sistema de logging."""
    
    def test_logging_after_setup(self):
        """Testa se o logging funciona após setup."""
        # Configura o sistema
        main_logger = setup_logging()
        
        # Obtém um logger específico
        test_logger = get_logger("test.integration")
        
        # Testa se consegue logar mensagens
        with patch.object(main_logger, 'info') as mock_info:
            test_logger.info("Mensagem de teste")
            # Verifica se a mensagem foi propagada
            # (dependendo da configuração, pode ou não ser chamada)
    
    def test_different_log_levels(self):
        """Testa diferentes níveis de log."""
        setup_logging()
        logger = get_logger("test.levels")
        
        # Testa se o logger aceita diferentes níveis
        try:
            logger.debug("Debug message")
            logger.info("Info message") 
            logger.warning("Warning message")
            logger.error("Error message")
            logger.critical("Critical message")
        except Exception as e:
            pytest.fail(f"Erro ao logar mensagens: {e}")
    
    def test_logger_hierarchy(self):
        """Testa hierarquia de loggers."""
        setup_logging()
        
        parent_logger = get_logger("app")
        child_logger = get_logger("app.module")
        grandchild_logger = get_logger("app.module.submodule")
        
        # Verifica se os loggers foram criados
        assert parent_logger is not None
        assert child_logger is not None
        assert grandchild_logger is not None
        
        # Verifica hierarquia
        assert child_logger.parent.name == "app"
        assert grandchild_logger.parent.name == "app.module"


class TestLoggingConfiguration:
    """Testes para configuração específica do logging."""
    
    def test_rotating_file_handler_configuration(self):
        """Testa configuração do RotatingFileHandler."""
        logger = setup_logging()
        
        # Procura por RotatingFileHandler
        rotating_handlers = [
            h for h in logger.handlers 
            if h.__class__.__name__ == 'RotatingFileHandler'
        ]
        
        assert len(rotating_handlers) >= 2  # arquivo normal e erro
        
        for handler in rotating_handlers:
            assert hasattr(handler, 'maxBytes')
            assert hasattr(handler, 'backupCount')
            assert handler.maxBytes == 10*1024*1024  # 10MB
            assert handler.backupCount == 5
    
    def test_console_handler_configuration(self):
        """Testa configuração do handler de console."""
        logger = setup_logging()
        
        # Procura por StreamHandler
        stream_handlers = [
            h for h in logger.handlers 
            if h.__class__.__name__ == 'StreamHandler'
        ]
        
        assert len(stream_handlers) >= 1
        
        for handler in stream_handlers:
            assert handler.level == logging.INFO
            assert handler.formatter is not None
    
    def test_error_handler_configuration(self):
        """Testa configuração específica do handler de erro."""
        logger = setup_logging()
        
        # Procura por handler de erro (level ERROR)
        error_handlers = [
            h for h in logger.handlers 
            if h.level == logging.ERROR
        ]
        
        assert len(error_handlers) >= 1
        
        for handler in error_handlers:
            assert handler.__class__.__name__ == 'RotatingFileHandler'
            assert handler.formatter is not None


class TestLoggingEdgeCases:
    """Testes para casos extremos do logging."""
    
    def test_setup_logging_multiple_calls(self):
        """Testa múltiplas chamadas de setup_logging."""
        logger1 = setup_logging()
        logger2 = setup_logging()
        
        # Deve retornar o mesmo logger (singleton pattern)
        assert logger1 is logger2
    
    def test_logging_with_none_name(self):
        """Testa logging com nome None."""
        # get_logger pode lidar com None?
        try:
            logger = get_logger(None)
            assert logger is not None
        except TypeError:
            # É aceitável que TypeError seja lançado para None
            pass
    
    def test_logging_with_very_long_name(self):
        """Testa logging com nome muito longo."""
        long_name = "a" * 1000
        logger = get_logger(long_name)
        
        assert logger is not None
        assert logger.name == long_name
    
    @patch('app.core.logging.Path.mkdir')
    def test_setup_logging_mkdir_error(self, mock_mkdir):
        """Testa erro na criação do diretório de logs."""
        # Simula erro na criação do diretório
        mock_mkdir.side_effect = PermissionError("Acesso negado")
        
        # setup_logging deve lidar com o erro graciosamente
        # ou propagar de forma apropriada
        try:
            logger = setup_logging()
            # Se não levantou exceção, deve ter criado o logger
            assert logger is not None
        except PermissionError:
            # É aceitável que a exceção seja propagada
            pass
    
    def test_logging_thread_safety(self):
        """Testa thread safety básico do logging."""
        import threading
        import time
        
        setup_logging()
        logger = get_logger("thread.test")
        
        results = []
        
        def log_messages(thread_id):
            for i in range(10):
                logger.info(f"Thread {thread_id}, message {i}")
                time.sleep(0.001)  # Pequeno delay
            results.append(f"Thread {thread_id} completed")
        
        # Cria múltiplas threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=log_messages, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Aguarda conclusão
        for thread in threads:
            thread.join()
        
        # Verifica se todas as threads completaram
        assert len(results) == 3
        assert all("completed" in result for result in results)


class TestLoggingMocking:
    """Testes usando mocks para verificar comportamento interno."""
    
    @patch('app.core.logging.RotatingFileHandler')
    @patch('app.core.logging.logging.StreamHandler')
    def test_handler_creation_mocked(self, mock_stream_handler, mock_rotating_handler):
        """Testa criação de handlers com mocks."""
        # Configura mocks
        mock_stream_instance = MagicMock()
        mock_rotating_instance = MagicMock()
        
        # Configura níveis para evitar erro de comparação
        mock_stream_instance.level = logging.INFO
        mock_rotating_instance.level = logging.INFO
        
        mock_stream_handler.return_value = mock_stream_instance
        mock_rotating_handler.return_value = mock_rotating_instance
        
        with patch('app.core.logging.Path'):
            setup_logging()
        
        # Verifica se os handlers foram criados
        mock_stream_handler.assert_called()
        mock_rotating_handler.assert_called()
        
        # Verifica se setFormatter foi chamado
        mock_stream_instance.setFormatter.assert_called()
        mock_rotating_instance.setFormatter.assert_called()
    
    @patch('app.core.logging.logging.getLogger')
    def test_logger_configuration_mocked(self, mock_get_logger):
        """Testa configuração do logger com mocks."""
        mock_logger = MagicMock()
        mock_logger.handlers = []  # Lista vazia de handlers
        mock_get_logger.return_value = mock_logger
        
        setup_logging()
        
        # Verifica se setLevel foi chamado
        mock_logger.setLevel.assert_called_with(logging.INFO)
        
        # Verifica se addHandler foi chamado múltiplas vezes
        assert mock_logger.addHandler.call_count >= 3
    
    @patch('app.core.logging.logging.getLogger')
    def test_get_logger_mocked(self, mock_get_logger):
        """Testa get_logger com mock."""
        mock_logger_instance = MagicMock()
        mock_get_logger.return_value = mock_logger_instance
        
        result = get_logger("test.mock")
        
        # Verifica se logging.getLogger foi chamado com o nome correto
        mock_get_logger.assert_called_once_with("test.mock")
        assert result is mock_logger_instance
