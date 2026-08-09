from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.pessoa_tea import PessoaTEA
from backend.models.usuario import Usuario
from backend.schemas.pessoa_tea import PessoaTEACreate, PessoaTEAPublic
from backend.auth.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=PessoaTEAPublic, status_code=status.HTTP_201_CREATED)
def criar_pessoa_tea(
    pessoa_tea: PessoaTEACreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    # O familia_id agora é pego do usuário autenticado, eliminando o ID fixo.
    db_pessoa_tea = PessoaTEA(**pessoa_tea.model_dump(), familia_id=current_user.familia_id)
    db.add(db_pessoa_tea)
    db.commit()
    db.refresh(db_pessoa_tea)
    return db_pessoa_tea

@router.get("/", response_model=List[PessoaTEAPublic])
def listar_pessoas_tea(
    db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)
):
    """Lista todas as Pessoas TEA pertencentes à família do usuário autenticado."""
    pessoas = (
        db.query(PessoaTEA).filter(PessoaTEA.familia_id == current_user.familia_id).all()
    )
    return pessoas