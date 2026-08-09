from typing import List

from pydantic import BaseModel

from .agenda import AgendaPublic
from .medicamento import MedicamentoPublic
from .receita_medica import ReceitaMedicaPublic


class DashboardStats(BaseModel):
    total_pessoas_tea: int
    total_medicamentos: int
    total_notificacoes_nao_lidas: int
    total_receitas: int
    total_compromissos: int
    medicamentos_criticos: List[MedicamentoPublic]
    receitas_vencendo: List[ReceitaMedicaPublic]
    receitas_vencidas: List[ReceitaMedicaPublic]
    compromissos_hoje: List[AgendaPublic]
    compromissos_semana: List[AgendaPublic]