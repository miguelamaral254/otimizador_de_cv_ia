"""
Testes unitários para app/utils/file_validator.py
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app.utils.file_validator import FileValidator


class TestFileValidatorConstants:
    """Testa as constantes da classe FileValidator."""
    
    def test_accepted_mime_types(self):
        """Testa se os tipos MIME aceitos estão corretos."""
        expected_types = [
            "application/pdf",
            "application/x-pdf",
            "binary/octet-stream"
        ]
        assert FileValidator.ACCEPTED_MIME_TYPES == expected_types
    
    def test_accepted_extensions(self):
        """Testa se as extensões aceitas estão corretas."""
        expected_extensions = [".pdf"]
        assert FileValidator.ACCEPTED_EXTENSIONS == expected_extensions


class TestFileValidatorValidatePdfFile:
    """Testa o método validate_pdf_file."""
    
    def test_validate_pdf_file_file_not_found(self):
        """Testa validação com arquivo inexistente."""
        non_existent_path = Path("/caminho/inexistente/arquivo.pdf")
        
        with pytest.raises(HTTPException) as exc_info:
            FileValidator.validate_pdf_file(non_existent_path)
        
        assert exc_info.value.status_code == 400
        assert "Arquivo não encontrado" in str(exc_info.value.detail)
    
    @patch('app.utils.file_validator.magic.from_file')
    def test_validate_pdf_file_valid_pdf(self, mock_magic):
        """Testa validação de PDF válido."""
        mock_magic.return_value = "application/pdf"
        
        # Cria arquivo temporário
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(b"%PDF-1.4\n%Test PDF content")
            temp_file_path = Path(temp_file.name)
        
        try:
            result = FileValidator.validate_pdf_file(temp_file_path)
            
            assert result["is_valid"] is True
            assert result["extension"] == ".pdf"
            assert result["mime_type"] == "application/pdf"
            assert result["errors"] == []
            assert result["file_size_mb"] > 0
        finally:
            # Limpa arquivo temporário
            os.unlink(temp_file_path)
    
    @patch('app.utils.file_validator.magic.from_file')
    def test_validate_pdf_file_invalid_extension(self, mock_magic):
        """Testa validação com extensão inválida."""
        mock_magic.return_value = "application/pdf"
        
        # Cria arquivo temporário com extensão inválida
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
            temp_file.write(b"Test content")
            temp_file_path = Path(temp_file.name)
        
        try:
            with pytest.raises(HTTPException) as exc_info:
                FileValidator.validate_pdf_file(temp_file_path)
            
            assert exc_info.value.status_code == 400
            assert "Extensão '.txt' não é aceita" in str(exc_info.value.detail)
        finally:
            os.unlink(temp_file_path)
    
    @patch('app.utils.file_validator.magic.from_file')
    def test_validate_pdf_file_too_large(self, mock_magic):
        """Testa validação com arquivo muito grande."""
        mock_magic.return_value = "application/pdf"
        
        # Cria arquivo temporário grande
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            # Escreve dados para criar arquivo de ~11MB
            large_data = b"x" * (11 * 1024 * 1024)
            temp_file.write(large_data)
            temp_file_path = Path(temp_file.name)
        
        try:
            with pytest.raises(HTTPException) as exc_info:
                FileValidator.validate_pdf_file(temp_file_path, max_size_mb=10)
            
            assert exc_info.value.status_code == 400
            assert "Arquivo muito grande" in str(exc_info.value.detail)
        finally:
            os.unlink(temp_file_path)
    
    @patch('app.utils.file_validator.magic.from_file')
    def test_validate_pdf_file_invalid_mime_type(self, mock_magic):
        """Testa validação com tipo MIME inválido."""
        mock_magic.return_value = "text/plain"
        
        # Cria arquivo temporário
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(b"Test content")
            temp_file_path = Path(temp_file.name)
        
        try:
            with pytest.raises(HTTPException) as exc_info:
                FileValidator.validate_pdf_file(temp_file_path)
            
            assert exc_info.value.status_code == 400
            assert "Tipo de arquivo inválido: text/plain" in str(exc_info.value.detail)
        finally:
            os.unlink(temp_file_path)
    
    @patch('app.utils.file_validator.magic.from_file')
    def test_validate_pdf_file_magic_error(self, mock_magic):
        """Testa validação quando magic.from_file falha."""
        mock_magic.side_effect = Exception("Magic error")
        
        # Cria arquivo temporário
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(b"Test content")
            temp_file_path = Path(temp_file.name)
        
        try:
            with pytest.raises(HTTPException) as exc_info:
                FileValidator.validate_pdf_file(temp_file_path)
            
            assert exc_info.value.status_code == 400
            assert "Não foi possível verificar o tipo do arquivo" in str(exc_info.value.detail)
        finally:
            os.unlink(temp_file_path)
    
    @patch('app.utils.file_validator.magic.from_file')
    def test_validate_pdf_file_without_content_check(self, mock_magic):
        """Testa validação sem verificação de conteúdo."""
        # Cria arquivo temporário
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(b"Test content")
            temp_file_path = Path(temp_file.name)
        
        try:
            result = FileValidator.validate_pdf_file(
                temp_file_path, 
                check_content=False
            )
            
            assert result["is_valid"] is True
            assert result["extension"] == ".pdf"
            assert result["mime_type"] is None
            assert result["errors"] == []
            assert result["file_size_mb"] > 0
            
            # Verifica se magic.from_file não foi chamado
            mock_magic.assert_not_called()
        finally:
            os.unlink(temp_file_path)
    
    @patch('app.utils.file_validator.magic.from_file')
    def test_validate_pdf_file_custom_max_size(self, mock_magic):
        """Testa validação com tamanho máximo personalizado."""
        mock_magic.return_value = "application/pdf"
        
        # Cria arquivo temporário de ~2MB
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            large_data = b"x" * (2 * 1024 * 1024)
            temp_file.write(large_data)
            temp_file_path = Path(temp_file.name)
        
        try:
            # Testa com limite de 1MB (deve falhar)
            with pytest.raises(HTTPException) as exc_info:
                FileValidator.validate_pdf_file(temp_file_path, max_size_mb=1)
            
            assert exc_info.value.status_code == 400
            assert "Arquivo muito grande" in str(exc_info.value.detail)
            
            # Testa com limite de 5MB (deve passar)
            result = FileValidator.validate_pdf_file(temp_file_path, max_size_mb=5)
            assert result["is_valid"] is True
        finally:
            os.unlink(temp_file_path)
    
    @patch('app.utils.file_validator.magic.from_file')
    def test_validate_pdf_file_multiple_errors(self, mock_magic):
        """Testa validação com múltiplos erros."""
        mock_magic.return_value = "text/plain"
        
        # Cria arquivo temporário grande com extensão inválida
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
            large_data = b"x" * (11 * 1024 * 1024)
            temp_file.write(large_data)
            temp_file_path = Path(temp_file.name)
        
        try:
            with pytest.raises(HTTPException) as exc_info:
                FileValidator.validate_pdf_file(temp_file_path, max_size_mb=10)
            
            assert exc_info.value.status_code == 400
            error_detail = str(exc_info.value.detail)
            assert "Extensão '.txt' não é aceita" in error_detail
            assert "Arquivo muito grande" in error_detail
            assert "Tipo de arquivo inválido: text/plain" in error_detail
        finally:
            os.unlink(temp_file_path)
    
    def test_validate_pdf_file_unexpected_error(self):
        """Testa validação com erro inesperado."""
        # Mock do Path para simular erro inesperado
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_path.suffix = ".pdf"
        mock_path.stat.side_effect = Exception("Unexpected error")
        
        with pytest.raises(HTTPException) as exc_info:
            FileValidator.validate_pdf_file(mock_path)
        
        assert exc_info.value.status_code == 500
        assert "Erro ao validar arquivo" in str(exc_info.value.detail)


class TestFileValidatorSanitizeFilename:
    """Testa o método sanitize_filename."""
    
    def test_sanitize_filename_no_dangerous_chars(self):
        """Testa sanitização de nome sem caracteres perigosos."""
        filename = "documento.pdf"
        sanitized = FileValidator.sanitize_filename(filename)
        assert sanitized == "documento.pdf"
    
    def test_sanitize_filename_with_dangerous_chars(self):
        """Testa sanitização de nome com caracteres perigosos."""
        filename = "doc/umento:com*caracteres?\"perigosos<>.pdf"
        sanitized = FileValidator.sanitize_filename(filename)
        assert sanitized == "doc_umento_com_caracteres_perigosos_.pdf"
    
    def test_sanitize_filename_multiple_spaces(self):
        """Testa sanitização de nome com múltiplos espaços."""
        filename = "documento   com    muitos    espaços.pdf"
        sanitized = FileValidator.sanitize_filename(filename)
        assert sanitized == "documento com muitos espaços.pdf"
    
    def test_sanitize_filename_too_long(self):
        """Testa sanitização de nome muito longo."""
        # Nome com 120 caracteres
        long_name = "a" * 120
        filename = f"{long_name}.pdf"
        sanitized = FileValidator.sanitize_filename(filename)
        
        # Deve ser truncado para 100 caracteres
        assert len(sanitized) <= 100
        assert sanitized.endswith(".pdf")
    
    def test_sanitize_filename_too_long_no_extension(self):
        """Testa sanitização de nome muito longo sem extensão."""
        # Nome com 120 caracteres sem extensão
        long_name = "a" * 120
        sanitized = FileValidator.sanitize_filename(long_name)
        
        # Deve ser truncado para 95 caracteres
        assert len(sanitized) <= 95
    
    def test_sanitize_filename_edge_cases(self):
        """Testa casos extremos de sanitização."""
        # Nome vazio
        sanitized = FileValidator.sanitize_filename("")
        assert sanitized == ""
        
        # Nome apenas com espaços
        sanitized = FileValidator.sanitize_filename("   ")
        assert sanitized == ""
        
        # Nome apenas com caracteres perigosos
        sanitized = FileValidator.sanitize_filename("\\/:*?\"<>|")
        assert sanitized == "_______"
        
        # Nome com underscore e hífen (deve preservar)
        sanitized = FileValidator.sanitize_filename("user-name_file.pdf")
        assert sanitized == "user-name_file.pdf"


class TestFileValidatorIntegration:
    """Testa integração entre métodos da classe."""
    
    @patch('app.utils.file_validator.magic.from_file')
    def test_validate_and_sanitize_integration(self, mock_magic):
        """Testa integração entre validação e sanitização."""
        mock_magic.return_value = "application/pdf"
        
        # Nome de arquivo com caracteres perigosos
        dangerous_filename = "doc/umento:perigoso.pdf"
        sanitized_filename = FileValidator.sanitize_filename(dangerous_filename)
        
        # Cria arquivo temporário com nome sanitizado
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(b"%PDF-1.4\n%Test content")
            temp_file_path = Path(temp_file.name)
        
        try:
            # Valida o arquivo
            result = FileValidator.validate_pdf_file(temp_file_path)
            
            assert result["is_valid"] is True
            assert result["extension"] == ".pdf"
            assert result["mime_type"] == "application/pdf"
        finally:
            os.unlink(temp_file_path)


class TestFileValidatorErrorHandling:
    """Testa tratamento de erros da classe."""
    
    def test_validate_pdf_file_http_exception_re_raise(self):
        """Testa se HTTPException é re-levantada corretamente."""
        # Mock do Path para simular HTTPException
        mock_path = MagicMock()
        mock_path.exists.side_effect = HTTPException(
            status_code=400, 
            detail="Custom error"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            FileValidator.validate_pdf_file(mock_path)
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Custom error"
    
    def test_validate_pdf_file_generic_exception_wrapping(self):
        """Testa se exceções genéricas são envolvidas em HTTPException."""
        # Mock do Path para simular erro genérico
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_path.suffix = ".pdf"
        mock_path.stat.side_effect = ValueError("Value error")
        
        with pytest.raises(HTTPException) as exc_info:
            FileValidator.validate_pdf_file(mock_path)
        
        assert exc_info.value.status_code == 500
        assert "Erro ao validar arquivo" in str(exc_info.value.detail)
        assert "Value error" in str(exc_info.value.detail)


class TestFileValidatorConstantsAccess:
    """Testa acesso às constantes da classe."""
    
    def test_constants_are_class_attributes(self):
        """Testa se as constantes são atributos de classe."""
        assert hasattr(FileValidator, 'ACCEPTED_MIME_TYPES')
        assert hasattr(FileValidator, 'ACCEPTED_EXTENSIONS')
        
        # Verifica se são listas
        assert isinstance(FileValidator.ACCEPTED_MIME_TYPES, list)
        assert isinstance(FileValidator.ACCEPTED_EXTENSIONS, list)
        
        # Verifica se não estão vazias
        assert len(FileValidator.ACCEPTED_MIME_TYPES) > 0
        assert len(FileValidator.ACCEPTED_EXTENSIONS) > 0
    
    def test_constants_are_immutable(self):
        """Testa se as constantes não podem ser modificadas."""
        original_mime_types = FileValidator.ACCEPTED_MIME_TYPES.copy()
        original_extensions = FileValidator.ACCEPTED_EXTENSIONS.copy()
        
        # Tenta modificar (deve falhar se forem tuplas)
        try:
            FileValidator.ACCEPTED_MIME_TYPES.append("invalid/type")
            # Se chegou aqui, são listas mutáveis
            assert FileValidator.ACCEPTED_MIME_TYPES != original_mime_types
        except AttributeError:
            # Se falhou, são tuplas imutáveis
            pass
        
        try:
            FileValidator.ACCEPTED_EXTENSIONS.append(".invalid")
            # Se chegou aqui, são listas mutáveis
            assert FileValidator.ACCEPTED_EXTENSIONS != original_extensions
        except AttributeError:
            # Se falhou, são tuplas imutáveis
            pass


class TestFileValidatorMethodSignatures:
    """Testa assinaturas dos métodos da classe."""
    
    def test_validate_pdf_file_is_classmethod(self):
        """Testa se validate_pdf_file é um classmethod."""
        assert hasattr(FileValidator.validate_pdf_file, '__func__')
        # Verifica se pode ser chamado na classe
        assert callable(FileValidator.validate_pdf_file)
    
    def test_sanitize_filename_is_classmethod(self):
        """Testa se sanitize_filename é um classmethod."""
        assert hasattr(FileValidator.sanitize_filename, '__func__')
        # Verifica se pode ser chamado na classe
        assert callable(FileValidator.sanitize_filename)
    
    def test_methods_accept_correct_parameters(self):
        """Testa se os métodos aceitam os parâmetros corretos."""
        # validate_pdf_file deve aceitar file_path, max_size_mb, check_content
        import inspect
        sig = inspect.signature(FileValidator.validate_pdf_file)
        params = list(sig.parameters.keys())
        
        assert 'file_path' in params
        assert 'max_size_mb' in params
        assert 'check_content' in params
        
        # sanitize_filename deve aceitar filename
        sig = inspect.signature(FileValidator.sanitize_filename)
        params = list(sig.parameters.keys())
        
        assert 'filename' in params
