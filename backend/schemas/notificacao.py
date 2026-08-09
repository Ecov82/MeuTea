from datetime import datetime

from pydantic import BaseModel


class NotificacaoPublic(BaseModel):
    id: int
    titulo: str
    mensagem: str
    data_envio: datetime
    lida: bool
    pessoa_tea_id: int

    class Config:
        from_attributes = True