from typing import Optional
from sqlalchemy.orm import Session

from backend.auth import security
from backend.models.usuario import Usuario


def get_user_by_email(db: Session, email: str) -> Optional[Usuario]:
    """Busca um usuário no banco de dados pelo seu email."""
    return db.query(Usuario).filter(Usuario.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[Usuario]:
    """Autentica um usuário, verificando email e senha."""
    user = get_user_by_email(db, email)
    if not user or not security.verify_password(password, user.senha_hash):
        return None
    return user