from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from backend.database import Base


class Notificacao(Base):
    __tablename__ = "notificacoes"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200))
    mensagem = Column(Text)
    data_envio = Column(TIMESTAMP, nullable=False)
    lida = Column(Boolean, default=False)
    pessoa_tea_id = Column(Integer, ForeignKey("pessoas_tea.id"))
    pessoa_tea = relationship("PessoaTEA", back_populates="notificacoes")