from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.database import Base


class PessoaTEA(Base):
    __tablename__ = "pessoas_tea"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    data_nascimento = Column(Date)
    nivel_suporte = Column(Integer)
    observacoes = Column(Text)
    familia_id = Column(Integer, ForeignKey("familias.id"))

    familia = relationship("Familia", back_populates="assistidos")
    medicamentos = relationship(
        "Medicamento", back_populates="pessoa_tea", cascade="all, delete-orphan"
    )
    notificacoes = relationship(
        "Notificacao", back_populates="pessoa_tea", cascade="all, delete-orphan"
    )
    receitas = relationship(
        "ReceitaMedica", back_populates="pessoa_tea", cascade="all, delete-orphan"
    )
    agenda = relationship("Agenda", back_populates="pessoa_tea", cascade="all, delete-orphan")