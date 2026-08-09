from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from backend.database import Base


class Medicamento(Base):
    __tablename__ = "medicamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    quantidade_atual = Column(Integer, nullable=False)
    uso_diario = Column(Integer, nullable=False)
    estoque_minimo = Column(Integer, nullable=False)
    horario = Column(String)
    observacoes = Column(Text)

    pessoa_tea_id = Column(Integer, ForeignKey("pessoas_tea.id"))

    pessoa_tea = relationship("PessoaTEA", back_populates="medicamentos")
    receitas = relationship("ReceitaMedica", back_populates="medicamento", cascade="all, delete-orphan")