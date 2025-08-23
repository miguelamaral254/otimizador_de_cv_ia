from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

# Configuração do esquema de autenticação
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Valida o token JWT e retorna o usuário atual.

    Args:
        credentials: Credenciais de autorização HTTP
        db: Sessão do banco de dados

    Returns:
        User: Usuário autenticado

    Raises:
        HTTPException: Se o token for inválido ou expirado
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o token JWT
        payload = jwt.decode(
            credentials.credentials,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        user_id: Optional[int] = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Busca o usuário no banco de dados
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Verifica se o usuário atual está ativo.

    Args:
        current_user: Usuário atual obtido via get_current_user

    Returns:
        User: Usuário ativo

    Raises:
        HTTPException: Se o usuário estiver inativo
    """
    # Aqui você pode adicionar lógica adicional para verificar
    # se o usuário está ativo, não foi banido, etc.
    return current_user


def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    """
    Cria um token de acesso JWT.

    Args:
        data: Dados a serem codificados no token
        expires_delta: Tempo de expiração em minutos

    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()

    if expires_delta:
        from datetime import datetime, timedelta

        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        from datetime import datetime, timedelta

        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )

    return encoded_jwt
