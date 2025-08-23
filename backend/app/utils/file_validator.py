"""
Utilitários para validação de arquivos.
"""

import magic
from pathlib import Path
from fastapi import HTTPException, status
from typing import Optional


class FileValidator:
    """Classe para validação de arquivos."""
    
    # Tipos MIME aceitos para PDFs
    ACCEPTED_MIME_TYPES = [
        "application/pdf",
        "application/x-pdf",
        "binary/octet-stream"  # Alguns PDFs podem ter este tipo
    ]
    
    # Extensões aceitas
    ACCEPTED_EXTENSIONS = [".pdf"]
    
    @classmethod
    def validate_pdf_file(
        cls,
        file_path: Path,
        max_size_mb: int = 10,
        check_content: bool = True
    ) -> dict:
        """
        Valida um arquivo PDF.
        
        Args:
            file_path: Caminho para o arquivo
            max_size_mb: Tamanho máximo em MB
            check_content: Se deve verificar o conteúdo do arquivo
            
        Returns:
            dict: Informações de validação
            
        Raises:
            HTTPException: Se o arquivo for inválido
        """
        validation_result = {
            "is_valid": True,
            "file_size_mb": 0,
            "mime_type": None,
            "extension": None,
            "errors": []
        }
        
        try:
            # Verifica se o arquivo existe
            if not file_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Arquivo não encontrado"
                )
            
            # Verifica extensão
            file_extension = file_path.suffix.lower()
            validation_result["extension"] = file_extension
            
            if file_extension not in cls.ACCEPTED_EXTENSIONS:
                validation_result["is_valid"] = False
                validation_result["errors"].append(
                    f"Extensão '{file_extension}' não é aceita. Use apenas: {', '.join(cls.ACCEPTED_EXTENSIONS)}"
                )
            
            # Verifica tamanho
            file_size_bytes = file_path.stat().st_size
            file_size_mb = file_size_bytes / (1024 * 1024)
            validation_result["file_size_mb"] = round(file_size_mb, 2)
            
            max_size_bytes = max_size_mb * 1024 * 1024
            if file_size_bytes > max_size_bytes:
                validation_result["is_valid"] = False
                validation_result["errors"].append(
                    f"Arquivo muito grande: {file_size_mb:.2f}MB. Tamanho máximo: {max_size_mb}MB"
                )
            
            # Verifica tipo MIME se solicitado
            if check_content:
                try:
                    mime_type = magic.from_file(str(file_path), mime=True)
                    validation_result["mime_type"] = mime_type
                    
                    if mime_type not in cls.ACCEPTED_MIME_TYPES:
                        validation_result["is_valid"] = False
                        validation_result["errors"].append(
                            f"Tipo de arquivo inválido: {mime_type}. Apenas PDFs são aceitos."
                        )
                except Exception as e:
                    validation_result["errors"].append(
                        f"Não foi possível verificar o tipo do arquivo: {str(e)}"
                    )
                    validation_result["is_valid"] = False
            
            # Se houver erros, levanta exceção
            if not validation_result["is_valid"]:
                error_message = "; ".join(validation_result["errors"])
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_message
                )
            
            return validation_result
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao validar arquivo: {str(e)}"
            )
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """
        Sanitiza o nome do arquivo para evitar problemas de segurança.
        
        Args:
            filename: Nome original do arquivo
            
        Returns:
            str: Nome sanitizado
        """
        # Remove caracteres perigosos
        dangerous_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        sanitized = filename
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '_')
        
        # Remove espaços múltiplos
        sanitized = ' '.join(sanitized.split())
        
        # Limita o tamanho
        if len(sanitized) > 100:
            name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
            sanitized = name[:95] + ('.' + ext if ext else '')
        
        return sanitized




