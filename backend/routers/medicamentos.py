from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database import get_db
from backend.models import Usuario
from backend.schemas.medicamento import (
    MedicamentoCreate,
    MedicamentoPublic,
    MedicamentoStatus,
    MedicamentoUpdate,
)
from backend.services import medicamento_service

router = APIRouter()


@router.post(
    "/", response_model=MedicamentoPublic, status_code=status.HTTP_201_CREATED
)
def create_medicamento(
    medicamento: MedicamentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return medicamento_service.create_medicamento(db, medicamento, current_user)


@router.get("/", response_model=List[MedicamentoPublic])
def get_all_medicamentos_from_family(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return medicamento_service.get_medicamentos_da_familia(db, current_user)


@router.get("/{medicamento_id}", response_model=MedicamentoPublic)
def get_medicamento(
    medicamento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return medicamento_service.get_medicamento_e_verificar_permissao(
        db, medicamento_id, current_user
    )


@router.get("/{medicamento_id}/status", response_model=MedicamentoStatus)
def get_medicamento_status(
    medicamento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    medicamento = medicamento_service.get_medicamento_e_verificar_permissao(
        db, medicamento_id, current_user
    )
    return medicamento_service.calcular_status_medicamento(medicamento)


@router.put("/{medicamento_id}", response_model=MedicamentoPublic)
def update_medicamento(
    medicamento_id: int,
    medicamento_update: MedicamentoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    medicamento_db = medicamento_service.get_medicamento_e_verificar_permissao(
        db, medicamento_id, current_user
    )
    return medicamento_service.update_medicamento(db, medicamento_db, medicamento_update)


@router.delete("/{medicamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medicamento(
    medicamento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    medicamento_db = medicamento_service.get_medicamento_e_verificar_permissao(
        db, medicamento_id, current_user
    )
    db.delete(medicamento_db)
    db.commit()