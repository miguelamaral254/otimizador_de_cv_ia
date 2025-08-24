"""
Utilitários para manipulação de arquivos.

Este módulo contém funções para validação, upload e processamento de arquivos.
"""

import os
import aiofiles
from typing import Optional
from fastapi import UploadFile, HTTPException, status
from pypdf import PdfReader
import io

async def extrair_texto_de_pdf(file: UploadFile) -> str:
    """
    Extrai texto de um arquivo PDF usando pypdf.
    
    Args:
        file: Arquivo PDF enviado via upload
        
    Returns:
        Texto extraído do PDF
        
    Raises:
        HTTPException: Se não for possível extrair o texto
    """
    try:
        # Lê o conteúdo do arquivo
        content = await file.read()
        
        # Cria um buffer de bytes para o PdfReader
        pdf_buffer = io.BytesIO(content)
        
        # Extrai texto usando pypdf
        pdf_reader = PdfReader(pdf_buffer)
        texto_completo = ""
        
        for page in pdf_reader.pages:
            texto_pagina = page.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina + "\n"
        
        # Reposiciona o cursor do arquivo para o início
        await file.seek(0)
        
        if not texto_completo.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O PDF não contém texto extraível"
            )
        
        return texto_completo.strip()
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao extrair texto do PDF: {str(e)}"
        )

def validar_arquivo_pdf(file: UploadFile) -> bool:
    """
    Valida se o arquivo é um PDF válido.
    
    Args:
        file: Arquivo enviado via upload
        
    Returns:
        True se o arquivo for válido
        
    Raises:
        HTTPException: Se o arquivo for inválido
    """
    # Verifica o tipo MIME
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de arquivo inválido. Apenas PDFs são aceitos."
        )
    
    # Verifica a extensão do arquivo
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de arquivo inválido. Deve terminar com .pdf"
        )
    
    # Verifica o tamanho do arquivo
    from app.core.config import settings
    if file.size and file.size > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Arquivo muito grande. Tamanho máximo: {settings.max_file_size / 1024 / 1024:.1f}MB"
        )
    
    return True

async def salvar_arquivo_pdf(
    file: UploadFile, 
    upload_dir: str, 
    filename: str
) -> str:
    """
    Salva um arquivo PDF no diretório de uploads.
    
    Args:
        file: Arquivo PDF enviado
        upload_dir: Diretório de destino
        filename: Nome do arquivo
        
    Returns:
        Caminho completo do arquivo salvo
    """
    # Cria o diretório se não existir
    os.makedirs(upload_dir, exist_ok=True)
    
    # Define o caminho completo
    file_path = os.path.join(upload_dir, filename)
    
    # Salva o arquivo
    async with aiofiles.open(file_path, 'wb') as buffer:
        content = await file.read()
        await buffer.write(content)
    
    # Reposiciona o cursor do arquivo
    await file.seek(0)
    
    return file_path

def obter_info_arquivo(file: UploadFile) -> dict:
    """
    Obtém informações básicas do arquivo.
    
    Args:
        file: Arquivo enviado
        
    Returns:
        Dicionário com informações do arquivo
    """
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size,
        "headers": dict(file.headers)
    }
