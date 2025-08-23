"""
Módulo de API para o Otimizador de Currículos com IA.

Este módulo contém as dependências e utilitários da API.
"""

from .dependencies import get_current_user, get_current_active_user, create_access_token

__all__ = [
    "get_current_user",
    "get_current_active_user", 
    "create_access_token"
]

