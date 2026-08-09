from typing import Optional

from pydantic import BaseModel


class MedicamentoBase(BaseModel):
    nome: str
    quantidade_atual: int
    uso_diario: int
    estoque_minimo: int
    horario: Optional[str] = None
    observacoes: Optional[str] = None


class MedicamentoCreate(MedicamentoBase):
    pessoa_tea_id: int


class MedicamentoUpdate(BaseModel):
    nome: Optional[str] = None
    quantidade_atual: Optional[int] = None
    uso_diario: Optional[int] = None
    estoque_minimo: Optional[int] = None
    horario: Optional[str] = None
    observacoes: Optional[str] = None


class MedicamentoPublic(MedicamentoBase):
    id: int
    pessoa_tea_id: int

    class Config:
        from_attributes = True


class MedicamentoStatus(BaseModel):
    dias_restantes: int
    status: str