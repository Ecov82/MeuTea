from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database import get_db
from backend.models import Usuario
from backend.schemas.agenda import (
    AgendaCreate,
    AgendaPublic,
    AgendaUpdate,
)
from backend.services import agenda_service

router = APIRouter(tags=["Agenda"])


@router.post("/", response_model=AgendaPublic, status_code=status.HTTP_201_CREATED)
def create_agendamento(
    agendamento: AgendaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return agenda_service.create_agendamento(db, agendamento, current_user)


@router.get("/", response_model=List[AgendaPublic])
def get_all_agendamentos_from_family(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return agenda_service.get_agendamentos_da_familia(db, current_user)


@router.get("/{agendamento_id}", response_model=AgendaPublic)
def get_agendamento(
    agendamento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return agenda_service.get_agendamento_e_verificar_permissao(
        db, agendamento_id, current_user
    )


@router.put("/{agendamento_id}", response_model=AgendaPublic)
def update_agendamento(
    agendamento_id: int,
    agendamento_update: AgendaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    agendamento_db = agenda_service.get_agendamento_e_verificar_permissao(
        db, agendamento_id, current_user
    )
    return agenda_service.update_agendamento(db, agendamento_db, agendamento_update)


@router.delete("/{agendamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agendamento(
    agendamento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    agendamento_db = agenda_service.get_agendamento_e_verificar_permissao(
        db, agendamento_id, current_user
    )
    db.delete(agendamento_db)
    db.commit()