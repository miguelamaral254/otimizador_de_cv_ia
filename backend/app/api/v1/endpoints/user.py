# backend/app/api/v1/endpoints/user.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserResponse
from passlib.context import CryptContext

router = APIRouter()

# Criamos um contexto para hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função auxiliar: transforma senha em hash
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Rota de criar usuário
@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar se já existe usuário com o mesmo email
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    # 2. Criar usuário novo com senha criptografada
    hashed_password = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    # 3. Salvar no banco
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
