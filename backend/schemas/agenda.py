from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from backend.models.agenda import StatusAgendamento, TipoAgendamento


class AgendaBase(BaseModel):
    titulo: str
    tipo: TipoAgendamento
    data_hora: datetime
    local: Optional[str] = None
    profissional: Optional[str] = None
    observacoes: Optional[str] = None


class AgendaCreate(AgendaBase):
    pessoa_tea_id: int


class AgendaUpdate(BaseModel):
    titulo: Optional[str] = None
    tipo: Optional[TipoAgendamento] = None
    data_hora: Optional[datetime] = None
    local: Optional[str] = None
    profissional: Optional[str] = None
    observacoes: Optional[str] = None
    status: Optional[StatusAgendamento] = None # This was correct, no change needed.


class AgendaPublic(AgendaBase):
    id: int
    pessoa_tea_id: int
    status: StatusAgendamento

    class Config:
        from_attributes = True