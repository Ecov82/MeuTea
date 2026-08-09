from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class Familia(Base):
    __tablename__ = "familias"

    id = Column(Integer, primary_key=True, index=True)
    nome_familia = Column(String(200), nullable=False, unique=True)

    # Relacionamentos bidirecionais com Usuario e PessoaTEA
    membros = relationship("Usuario", back_populates="familia")
    assistidos = relationship("PessoaTEA", back_populates="familia")