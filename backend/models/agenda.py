import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.database import Base


class TipoAgendamento(str, enum.Enum):
    consulta = "Consulta"
    terapia = "Terapia"
    escola = "Escola"
    outro = "Outro"


class StatusAgendamento(str, enum.Enum):
    agendado = "Agendado"
    realizado = "Realizado"
    cancelado = "Cancelado"


class Agenda(Base):
    __tablename__ = "agenda"

    id = Column(Integer, primary_key=True, index=True)
    pessoa_tea_id = Column(Integer, ForeignKey("pessoas_tea.id"), nullable=False)
    titulo = Column(String, nullable=False)
    tipo = Column(Enum(TipoAgendamento), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    local = Column(String)
    profissional = Column(String)
    observacoes = Column(Text)
    status = Column(Enum(StatusAgendamento), nullable=False, default=StatusAgendamento.agendado)

    pessoa_tea = relationship("PessoaTEA", back_populates="agenda")