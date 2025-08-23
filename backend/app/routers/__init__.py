"""
Módulo de routers para o Otimizador de Currículos com IA.

Este módulo contém os routers da aplicação.
"""

from .auth import router as auth_router
from .curriculum import router as curriculum_router
from .metrics import router as metrics_router

__all__ = [
    "auth_router",
    "curriculum_router", 
    "metrics_router"
]
