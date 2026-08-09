from datetime import date
from typing import Optional

from pydantic import BaseModel


class PessoaTEABase(BaseModel):
    nome: str
    data_nascimento: Optional[date] = None
    nivel_suporte: Optional[int] = None
    observacoes: Optional[str] = None


class PessoaTEACreate(PessoaTEABase):
    pass


class PessoaTEAPublic(PessoaTEABase):
    id: int
    familia_id: int

    class Config:
        from_attributes = True