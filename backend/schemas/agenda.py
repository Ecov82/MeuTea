from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AgendaBase(BaseModel):
    titulo: str
    tipo: str
    data_hora: datetime
    local: Optional[str] = None
    profissional: Optional[str] = None
    observacoes: Optional[str] = None
    status: Optional[str] = "Agendado"


class AgendaCreate(AgendaBase):
    pessoa_tea_id: int


class AgendaUpdate(BaseModel):
    titulo: Optional[str] = None
    tipo: Optional[str] = None
    data_hora: Optional[datetime] = None
    local: Optional[str] = None
    profissional: Optional[str] = None
    observacoes: Optional[str] = None
    status: Optional[str] = None


class AgendaPublic(AgendaBase):
    id: int
    pessoa_tea_id: int

    class Config:
        from_attributes = True