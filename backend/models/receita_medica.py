from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base


class ReceitaMedica(Base):
    __tablename__ = "receitas_medicas"

    id = Column(Integer, primary_key=True, index=True)
    pessoa_tea_id = Column(Integer, ForeignKey("pessoas_tea.id"), nullable=False)
    medicamento_id = Column(Integer, ForeignKey("medicamentos.id"), nullable=False)

    medico = Column(String, nullable=False)
    crm = Column(String)
    data_emissao = Column(Date, nullable=False)
    data_validade = Column(Date)
    arquivo_pdf = Column(String)  # Armazenará o caminho para o arquivo
    observacoes = Column(Text)

    # Relacionamentos
    pessoa_tea = relationship("PessoaTEA", back_populates="receitas")
    medicamento = relationship("Medicamento", back_populates="receitas")