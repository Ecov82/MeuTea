from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database import get_db
from backend.models import Usuario
from backend.schemas.receita_medica import (
    ReceitaMedicaCreate,
    ReceitaMedicaPublic,
    ReceitaMedicaUpdate,
)
from backend.services import receita_service

router = APIRouter(tags=["Receitas Médicas"])


@router.post("/", response_model=ReceitaMedicaPublic, status_code=status.HTTP_201_CREATED)
def create_receita(
    receita: ReceitaMedicaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return receita_service.create_receita(db, receita, current_user)


@router.get("/", response_model=List[ReceitaMedicaPublic])
def get_all_receitas_from_family(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return receita_service.get_receitas_da_familia(db, current_user)


@router.get("/{receita_id}", response_model=ReceitaMedicaPublic)
def get_receita(
    receita_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return receita_service.get_receita_e_verificar_permissao(db, receita_id, current_user)


@router.put("/{receita_id}", response_model=ReceitaMedicaPublic)
def update_receita(
    receita_id: int,
    receita_update: ReceitaMedicaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    receita_db = receita_service.get_receita_e_verificar_permissao(
        db, receita_id, current_user
    )
    return receita_service.update_receita(db, receita_db, receita_update)


@router.delete("/{receita_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_receita(
    receita_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    receita_db = receita_service.get_receita_e_verificar_permissao(
        db, receita_id, current_user
    )
    db.delete(receita_db)
    db.commit()