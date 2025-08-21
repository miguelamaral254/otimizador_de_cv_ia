from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Schema base para usuários."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)


class UserCreate(UserBase):
    """Schema para criação de usuário."""
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username deve conter apenas letras, números, underscore e hífen')
        return v


class UserUpdate(BaseModel):
    """Schema para atualização de usuário."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if v is not None and not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username deve conter apenas letras, números, underscore e hífen')
        return v


class UserResponse(UserBase):
    """Schema para resposta de usuário."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema para login de usuário."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema para token de autenticação."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # Em segundos


class TokenData(BaseModel):
    """Schema para dados do token decodificado."""
    email: Optional[str] = None
    user_id: Optional[int] = None
