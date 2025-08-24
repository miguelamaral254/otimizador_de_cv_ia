"""
Testes unitários para os utilitários de arquivo.
"""

import pytest
import io
import os
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from fastapi import HTTPException, status
from pypdf import PdfReader
from app.utils.file_utils import (
    extrair_texto_de_pdf,
    validar_arquivo_pdf,
    salvar_arquivo_pdf,
    obter_info_arquivo
)


class TestExtrairTextoDePdf:
    """Testes para a função extrair_texto_de_pdf."""
    
    @pytest.mark.asyncio
    async def test_extrair_texto_de_pdf_sucesso(self):
        """Testa a extração bem-sucedida de texto de um PDF."""
        # Mock do arquivo PDF
        mock_file = AsyncMock()
        mock_file.read.return_value = b"PDF content"
        mock_file.seek = AsyncMock()
        
        # Mock do PdfReader
        mock_page = Mock()
        mock_page.extract_text.return_value = "Texto da página"
        mock_pdf_reader = Mock()
        mock_pdf_reader.pages = [mock_page]
        
        with patch('app.utils.file_utils.PdfReader', return_value=mock_pdf_reader):
            resultado = await extrair_texto_de_pdf(mock_file)
            
            assert resultado == "Texto da página"
            mock_file.read.assert_called_once()
            mock_file.seek.assert_called_once_with(0)
    
    @pytest.mark.asyncio
    async def test_extrair_texto_de_pdf_multiplas_paginas(self):
        """Testa a extração de texto de um PDF com múltiplas páginas."""
        mock_file = AsyncMock()
        mock_file.read.return_value = b"PDF content"
        mock_file.seek = AsyncMock()
        
        # Mock de múltiplas páginas
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Página 1"
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Página 2"
        mock_pdf_reader = Mock()
        mock_pdf_reader.pages = [mock_page1, mock_page2]
        
        with patch('app.utils.file_utils.PdfReader', return_value=mock_pdf_reader):
            resultado = await extrair_texto_de_pdf(mock_file)
            
            assert resultado == "Página 1\nPágina 2"
    
    @pytest.mark.asyncio
    async def test_extrair_texto_de_pdf_sem_texto(self):
        """Testa a extração de um PDF sem texto extraível."""
        mock_file = AsyncMock()
        mock_file.read.return_value = b"PDF content"
        mock_file.seek = AsyncMock()
        
        # Mock de página sem texto
        mock_page = Mock()
        mock_page.extract_text.return_value = ""
        mock_pdf_reader = Mock()
        mock_pdf_reader.pages = [mock_page]
        
        with patch('app.utils.file_utils.PdfReader', return_value=mock_pdf_reader):
            with pytest.raises(HTTPException) as exc_info:
                await extrair_texto_de_pdf(mock_file)
            
            assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
            assert "O PDF não contém texto extraível" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_extrair_texto_de_pdf_erro_leitura(self):
        """Testa o tratamento de erro na leitura do arquivo."""
        mock_file = AsyncMock()
        mock_file.read.side_effect = Exception("Erro de leitura")
        
        with pytest.raises(HTTPException) as exc_info:
            await extrair_texto_de_pdf(mock_file)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Erro ao extrair texto do PDF" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_extrair_texto_de_pdf_erro_pypdf(self):
        """Testa o tratamento de erro do PdfReader."""
        mock_file = AsyncMock()
        mock_file.read.return_value = b"PDF content"
        mock_file.seek = AsyncMock()
        
        with patch('app.utils.file_utils.PdfReader', side_effect=Exception("Erro do PdfReader")):
            with pytest.raises(HTTPException) as exc_info:
                await extrair_texto_de_pdf(mock_file)
            
            assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
            assert "Erro ao extrair texto do PDF" in str(exc_info.value.detail)


class TestValidarArquivoPdf:
    """Testes para a função validar_arquivo_pdf."""
    
    def test_validar_arquivo_pdf_valido(self):
        """Testa a validação de um arquivo PDF válido."""
        mock_file = Mock()
        mock_file.content_type = "application/pdf"
        mock_file.filename = "documento.pdf"
        mock_file.size = 1024
        
        with patch('app.core.config.settings') as mock_settings:
            mock_settings.max_file_size = 10485760  # 10MB
            resultado = validar_arquivo_pdf(mock_file)
            
            assert resultado is True
    
    def test_validar_arquivo_pdf_tipo_mime_invalido(self):
        """Testa a validação com tipo MIME inválido."""
        mock_file = Mock()
        mock_file.content_type = "text/plain"
        mock_file.filename = "documento.pdf"
        
        with pytest.raises(HTTPException) as exc_info:
            validar_arquivo_pdf(mock_file)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Formato de arquivo inválido" in str(exc_info.value.detail)
    
    def test_validar_arquivo_pdf_extensao_invalida(self):
        """Testa a validação com extensão de arquivo inválida."""
        mock_file = Mock()
        mock_file.content_type = "application/pdf"
        mock_file.filename = "documento.txt"
        
        with pytest.raises(HTTPException) as exc_info:
            validar_arquivo_pdf(mock_file)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Nome de arquivo inválido" in str(exc_info.value.detail)
    
    def test_validar_arquivo_pdf_tamanho_excedido(self):
        """Testa a validação com arquivo muito grande."""
        mock_file = Mock()
        mock_file.content_type = "application/pdf"
        mock_file.filename = "documento.pdf"
        mock_file.size = 10485760  # 10MB
        
        with patch('app.core.config.settings') as mock_settings:
            mock_settings.max_file_size = 1048576  # 1MB
            with pytest.raises(HTTPException) as exc_info:
                validar_arquivo_pdf(mock_file)
            
            assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
            assert "Arquivo muito grande" in str(exc_info.value.detail)
    
    def test_validar_arquivo_pdf_sem_tamanho(self):
        """Testa a validação de arquivo sem informação de tamanho."""
        mock_file = Mock()
        mock_file.content_type = "application/pdf"
        mock_file.filename = "documento.pdf"
        mock_file.size = None
        
        with patch('app.core.config.settings') as mock_settings:
            mock_settings.max_file_size = 1048576  # 1MB
            resultado = validar_arquivo_pdf(mock_file)
            
            assert resultado is True
    
    def test_validar_arquivo_pdf_extensao_case_insensitive(self):
        """Testa a validação com extensão em maiúsculas."""
        mock_file = Mock()
        mock_file.content_type = "application/pdf"
        mock_file.filename = "DOCUMENTO.PDF"
        mock_file.size = 1024
        
        with patch('app.core.config.settings') as mock_settings:
            mock_settings.max_file_size = 10485760  # 10MB
            resultado = validar_arquivo_pdf(mock_file)
            
            assert resultado is True


class TestSalvarArquivoPdf:
    """Testes para a função salvar_arquivo_pdf."""
    
    @pytest.mark.asyncio
    async def test_salvar_arquivo_pdf_sucesso(self):
        """Testa o salvamento bem-sucedido de um arquivo PDF."""
        mock_file = AsyncMock()
        mock_file.read.return_value = b"PDF content"
        mock_file.seek = AsyncMock()
        
        upload_dir = "/tmp/uploads"
        filename = "test.pdf"
        
        with patch('app.utils.file_utils.os.makedirs') as mock_makedirs, \
             patch('app.utils.file_utils.aiofiles.open') as mock_open:
            
            mock_file_handle = AsyncMock()
            mock_open.return_value.__aenter__.return_value = mock_file_handle
            
            resultado = await salvar_arquivo_pdf(mock_file, upload_dir, filename)
            
            expected_path = os.path.join(upload_dir, filename)
            assert resultado == expected_path
            mock_makedirs.assert_called_once_with(upload_dir, exist_ok=True)
            mock_file.read.assert_called_once()
            mock_file_handle.write.assert_called_once_with(b"PDF content")
            mock_file.seek.assert_called_once_with(0)
    
    @pytest.mark.asyncio
    async def test_salvar_arquivo_pdf_cria_diretorio(self):
        """Testa se o diretório é criado quando não existe."""
        mock_file = AsyncMock()
        mock_file.read.return_value = b"PDF content"
        mock_file.seek = AsyncMock()
        
        upload_dir = "/tmp/novo_diretorio"
        filename = "test.pdf"
        
        with patch('app.utils.file_utils.os.makedirs') as mock_makedirs, \
             patch('app.utils.file_utils.aiofiles.open') as mock_open:
            
            mock_file_handle = AsyncMock()
            mock_open.return_value.__aenter__.return_value = mock_file_handle
            
            await salvar_arquivo_pdf(mock_file, upload_dir, filename)
            
            mock_makedirs.assert_called_once_with(upload_dir, exist_ok=True)
    
    @pytest.mark.asyncio
    async def test_salvar_arquivo_pdf_erro_escrita(self):
        """Testa o tratamento de erro na escrita do arquivo."""
        mock_file = AsyncMock()
        mock_file.read.return_value = b"PDF content"
        
        upload_dir = "/tmp/uploads"
        filename = "test.pdf"
        
        with patch('app.utils.file_utils.os.makedirs'), \
             patch('app.utils.file_utils.aiofiles.open', side_effect=Exception("Erro de escrita")):
            
            with pytest.raises(Exception) as exc_info:
                await salvar_arquivo_pdf(mock_file, upload_dir, filename)
            
            assert "Erro de escrita" in str(exc_info.value)


class TestObterInfoArquivo:
    """Testes para a função obter_info_arquivo."""
    
    def test_obter_info_arquivo_completo(self):
        """Testa a obtenção de informações de um arquivo completo."""
        mock_file = Mock()
        mock_file.filename = "documento.pdf"
        mock_file.content_type = "application/pdf"
        mock_file.size = 1024
        mock_file.headers = {"content-disposition": "attachment"}
        
        resultado = obter_info_arquivo(mock_file)
        
        expected = {
            "filename": "documento.pdf",
            "content_type": "application/pdf",
            "size": 1024,
            "headers": {"content-disposition": "attachment"}
        }
        assert resultado == expected
    
    def test_obter_info_arquivo_sem_headers(self):
        """Testa a obtenção de informações de arquivo sem headers."""
        mock_file = Mock()
        mock_file.filename = "documento.pdf"
        mock_file.content_type = "application/pdf"
        mock_file.size = 1024
        mock_file.headers = {}
        
        resultado = obter_info_arquivo(mock_file)
        
        expected = {
            "filename": "documento.pdf",
            "content_type": "application/pdf",
            "size": 1024,
            "headers": {}
        }
        assert resultado == expected
    
    def test_obter_info_arquivo_sem_tamanho(self):
        """Testa a obtenção de informações de arquivo sem tamanho."""
        mock_file = Mock()
        mock_file.filename = "documento.pdf"
        mock_file.content_type = "application/pdf"
        mock_file.size = None
        mock_file.headers = {}
        
        resultado = obter_info_arquivo(mock_file)
        
        expected = {
            "filename": "documento.pdf",
            "content_type": "application/pdf",
            "size": None,
            "headers": {}
        }
        assert resultado == expected
    
    def test_obter_info_arquivo_headers_convertidos(self):
        """Testa se os headers são convertidos para dict."""
        mock_file = Mock()
        mock_file.filename = "documento.pdf"
        mock_file.content_type = "application/pdf"
        mock_file.size = 1024
        
        # Cria um objeto que simula headers não-dict mas iterável
        class MockHeaders:
            def __init__(self):
                self.content_disposition = "attachment"
            
            def __iter__(self):
                return iter([("content-disposition", "attachment")])
        
        mock_file.headers = MockHeaders()
        
        resultado = obter_info_arquivo(mock_file)
        
        assert "headers" in resultado
        assert isinstance(resultado["headers"], dict)


class TestFileUtilsIntegration:
    """Testes de integração entre as funções."""
    
    @pytest.mark.asyncio
    async def test_fluxo_completo_upload_pdf(self):
        """Testa o fluxo completo de upload e validação de PDF."""
        # Cria um mock de arquivo PDF válido
        mock_file = AsyncMock()
        mock_file.filename = "documento.pdf"
        mock_file.content_type = "application/pdf"
        mock_file.size = 1024
        mock_file.headers = {}
        mock_file.read.return_value = b"PDF content"
        mock_file.seek = AsyncMock()
        
        # Valida o arquivo
        with patch('app.core.config.settings') as mock_settings:
            mock_settings.max_file_size = 10485760  # 10MB
            validar_arquivo_pdf(mock_file)
        
        # Obtém informações do arquivo
        info = obter_info_arquivo(mock_file)
        assert info["filename"] == "documento.pdf"
        assert info["content_type"] == "application/pdf"
        
        # Extrai texto do PDF
        with patch('app.utils.file_utils.PdfReader') as mock_pdf_reader:
            mock_page = Mock()
            mock_page.extract_text.return_value = "Texto do PDF"
            mock_pdf_reader.return_value.pages = [mock_page]
            
            texto = await extrair_texto_de_pdf(mock_file)
            assert texto == "Texto do PDF"
    
    def test_validacao_arquivo_invalido(self):
        """Testa a validação de arquivo inválido em diferentes aspectos."""
        # Arquivo com tipo MIME inválido
        mock_file1 = Mock()
        mock_file1.content_type = "text/plain"
        mock_file1.filename = "documento.pdf"
        mock_file1.size = 1024
        
        with pytest.raises(HTTPException) as exc_info:
            validar_arquivo_pdf(mock_file1)
        assert "Formato de arquivo inválido" in str(exc_info.value.detail)
        
        # Arquivo com extensão inválida
        mock_file2 = Mock()
        mock_file2.content_type = "application/pdf"
        mock_file2.filename = "documento.txt"
        mock_file2.size = 1024
        
        with pytest.raises(HTTPException) as exc_info:
            validar_arquivo_pdf(mock_file2)
        assert "Nome de arquivo inválido" in str(exc_info.value.detail)
        
        # Arquivo muito grande
        mock_file3 = Mock()
        mock_file3.content_type = "application/pdf"
        mock_file3.filename = "documento.pdf"
        mock_file3.size = 10485760  # 10MB
        
        with patch('app.core.config.settings') as mock_settings:
            mock_settings.max_file_size = 1048576  # 1MB
            with pytest.raises(HTTPException) as exc_info:
                validar_arquivo_pdf(mock_file3)
            assert "Arquivo muito grande" in str(exc_info.value.detail)
