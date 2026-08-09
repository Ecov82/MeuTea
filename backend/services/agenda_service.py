from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.models import Agenda, PessoaTEA, Usuario
from backend.schemas.agenda import AgendaCreate, AgendaUpdate


def get_agendamento_e_verificar_permissao(
    db: Session, agendamento_id: int, current_user: Usuario
) -> Agenda:
    """Busca um agendamento e verifica se o usuário tem permissão para acessá-lo."""
    agendamento = (
        db.query(Agenda)
        .join(PessoaTEA)
        .filter(
            Agenda.id == agendamento_id,
            PessoaTEA.familia_id == current_user.familia_id,
        )
        .first()
    )
    if not agendamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento não encontrado"
        )
    return agendamento


def create_agendamento(
    db: Session, agendamento: AgendaCreate, current_user: Usuario
) -> Agenda:
    """Cria um novo agendamento para uma PessoaTEA da família do usuário."""
    pessoa_tea = db.query(PessoaTEA).filter(
        PessoaTEA.id == agendamento.pessoa_tea_id,
        PessoaTEA.familia_id == current_user.familia_id,
    ).first()
    if not pessoa_tea:
        raise HTTPException(status_code=404, detail="PessoaTEA not found in this family")

    db_agendamento = Agenda(**agendamento.model_dump())
    db.add(db_agendamento)
    db.commit()
    db.refresh(db_agendamento)
    return db_agendamento


def get_agendamentos_da_familia(db: Session, current_user: Usuario) -> List[Agenda]:
    """Retorna todos os agendamentos associados à família do usuário."""
    return (
        db.query(Agenda)
        .join(PessoaTEA)
        .filter(PessoaTEA.familia_id == current_user.familia_id)
        .order_by(Agenda.data_hora.asc())
        .all()
    )


def update_agendamento(
    db: Session, agendamento: Agenda, data_update: AgendaUpdate
) -> Agenda:
    """Atualiza os dados de um agendamento."""
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(agendamento, key, value)
    db.commit()
    db.refresh(agendamento)
    return agendamento