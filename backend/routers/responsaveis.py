from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.usuario import UsuarioCreate, UsuarioPublic
from backend.services import usuario_service
from backend.auth.dependencies import get_current_user
from backend.auth.security import get_password_hash
from backend.models.usuario import Usuario

router = APIRouter()


@router.post("/", response_model=UsuarioPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    """Endpoint para registrar um novo usuário (responsável)."""
    db_user = usuario_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.senha)
    db_user = Usuario(
        email=user.email,
        nome=user.nome,
        senha_hash=hashed_password,
        familia_id=user.familia_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/me", response_model=UsuarioPublic)
async def read_users_me(current_user: Usuario = Depends(get_current_user)):
    """Endpoint protegido que retorna os dados do usuário autenticado."""
    return current_user