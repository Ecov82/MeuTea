from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_pessoas_tea: int
    total_medicamentos: int
    total_receitas: int
    total_compromissos: int
    total_notificacoes_nao_lidas: int