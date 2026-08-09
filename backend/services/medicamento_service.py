from datetime import date, timedelta
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.models import Medicamento, PessoaTEA, Usuario
from backend.schemas.medicamento import MedicamentoCreate, MedicamentoUpdate


def _verificar_permissao_pessoa_tea(db: Session, pessoa_tea_id: int, familia_id: int):
    """Verifica se a PessoaTEA pertence à família do usuário."""
    pessoa_tea = db.query(PessoaTEA).filter(PessoaTEA.id == pessoa_tea_id).first()
    if not pessoa_tea or pessoa_tea.familia_id != familia_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PessoaTEA not found or does not belong to this family",
        )
    return pessoa_tea


def get_medicamento_e_verificar_permissao(
    db: Session, medicamento_id: int, current_user: Usuario
) -> Medicamento:
    """Busca um medicamento e verifica se o usuário tem permissão para acessá-lo."""
    medicamento = (
        db.query(Medicamento)
        .join(PessoaTEA)
        .filter(
            Medicamento.id == medicamento_id,
            PessoaTEA.familia_id == current_user.familia_id,
        )
        .first()
    )
    if not medicamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Medicamento not found"
        )
    return medicamento


def create_medicamento(
    db: Session, medicamento: MedicamentoCreate, current_user: Usuario
) -> Medicamento:
    """Cria um novo medicamento para uma PessoaTEA da família do usuário."""
    _verificar_permissao_pessoa_tea(
        db, pessoa_tea_id=medicamento.pessoa_tea_id, familia_id=current_user.familia_id
    )
    db_medicamento = Medicamento(**medicamento.model_dump())
    db.add(db_medicamento)
    db.commit()
    db.refresh(db_medicamento)
    return db_medicamento


def get_medicamentos_da_familia(db: Session, current_user: Usuario) -> List[Medicamento]:
    """Retorna todos os medicamentos associados à família do usuário."""
    return (
        db.query(Medicamento)
        .join(PessoaTEA)
        .filter(PessoaTEA.familia_id == current_user.familia_id)
        .all()
    )


def update_medicamento(
    db: Session, medicamento: Medicamento, data_update: MedicamentoUpdate
) -> Medicamento:
    """Atualiza os dados de um medicamento."""
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(medicamento, key, value)
    db.commit()
    db.refresh(medicamento)
    return medicamento


def calcular_status_medicamento(medicamento: Medicamento) -> dict:
    """Calcula os dias restantes e o status do estoque de um medicamento."""
    dias_restantes = None
    if medicamento.uso_diario > 0:
        dias_restantes = medicamento.quantidade_atual // medicamento.uso_diario

    if medicamento.quantidade_atual <= 0:
        status_estoque = "ESGOTADO"
    elif medicamento.quantidade_atual <= medicamento.estoque_minimo:
        status_estoque = "CRÍTICO"
    else:
        status_estoque = "NORMAL"

    return {"dias_restantes": dias_restantes, "status": status_estoque}