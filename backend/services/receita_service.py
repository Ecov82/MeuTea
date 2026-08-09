from datetime import date, timedelta
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.models import Medicamento, PessoaTEA, ReceitaMedica, Usuario
from backend.schemas.receita_medica import ReceitaMedicaCreate, ReceitaMedicaUpdate


def get_receita_e_verificar_permissao(
    db: Session, receita_id: int, current_user: Usuario
) -> ReceitaMedica:
    """Busca uma receita e verifica se o usuário tem permissão para acessá-la."""
    receita = (
        db.query(ReceitaMedica)
        .join(PessoaTEA)
        .filter(
            ReceitaMedica.id == receita_id,
            PessoaTEA.familia_id == current_user.familia_id,
        )
        .first()
    )
    if not receita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Receita não encontrada"
        )
    return receita


def create_receita(
    db: Session, receita: ReceitaMedicaCreate, current_user: Usuario
) -> ReceitaMedica:
    """Cria uma nova receita para uma PessoaTEA da família do usuário."""
    # Verifica se a PessoaTEA pertence à família
    pessoa_tea = db.query(PessoaTEA).filter(
        PessoaTEA.id == receita.pessoa_tea_id,
        PessoaTEA.familia_id == current_user.familia_id,
    ).first()
    if not pessoa_tea:
        raise HTTPException(status_code=404, detail="PessoaTEA not found in this family")

    # Verifica se o Medicamento pertence à família
    medicamento = db.query(Medicamento).join(PessoaTEA).filter(
        Medicamento.id == receita.medicamento_id,
        PessoaTEA.familia_id == current_user.familia_id,
    ).first()
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento not found in this family")

    # Garante que o medicamento está associado à PessoaTEA correta
    if medicamento.pessoa_tea_id != pessoa_tea.id:
        raise HTTPException(status_code=400, detail="Medicamento is not associated with the specified PessoaTEA")

    db_receita = ReceitaMedica(**receita.model_dump())
    db.add(db_receita)
    db.commit()
    db.refresh(db_receita)
    return db_receita


def get_receitas_da_familia(db: Session, current_user: Usuario) -> List[ReceitaMedica]:
    """Retorna todas as receitas associadas à família do usuário."""
    return (
        db.query(ReceitaMedica)
        .join(PessoaTEA)
        .filter(PessoaTEA.familia_id == current_user.familia_id)
        .all()
    )


def calcular_status_receita(receita: ReceitaMedica) -> dict:
    """Calcula os dias restantes e o status de validade de uma receita."""
    if not receita.data_validade:
        return {"dias_para_vencer": None, "status": "INDETERMINADO"}

    hoje = date.today()
    dias_para_vencer = (receita.data_validade - hoje).days

    if dias_para_vencer < 0: status_receita = "VENCIDA"
    elif dias_para_vencer <= 15: status_receita = "CRÍTICO"
    elif dias_para_vencer <= 30: status_receita = "ALERTA"
    else: status_receita = "NORMAL"

    return {"dias_para_vencer": dias_para_vencer, "status": status_receita}