from datetime import date
from typing import Optional

from pydantic import BaseModel


class ReceitaMedicaBase(BaseModel):
    medico: str
    crm: Optional[str] = None
    data_emissao: date
    data_validade: Optional[date] = None
    arquivo_pdf: Optional[str] = None
    observacoes: Optional[str] = None


class ReceitaMedicaCreate(ReceitaMedicaBase):
    pessoa_tea_id: int
    medicamento_id: int


class ReceitaMedicaUpdate(BaseModel):
    medico: Optional[str] = None
    crm: Optional[str] = None
    data_emissao: Optional[date] = None
    data_validade: Optional[date] = None
    arquivo_pdf: Optional[str] = None
    observacoes: Optional[str] = None


class ReceitaMedicaPublic(ReceitaMedicaBase):
    id: int
    pessoa_tea_id: int
    medicamento_id: int

    class Config:
        from_attributes = True