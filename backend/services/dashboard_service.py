from datetime import date, timedelta
from sqlalchemy.orm import Session

from backend.models import Agenda, Medicamento, Notificacao, PessoaTEA, ReceitaMedica, Usuario
from backend.services import medicamento_service, receita_service


def get_dashboard_stats(db: Session, current_user: Usuario):
    """Coleta estatísticas do dashboard para a família do usuário autenticado."""
    familia_id = current_user.familia_id

    total_pessoas_tea = db.query(PessoaTEA).filter(PessoaTEA.familia_id == familia_id).count()

    medicamentos_familia = (
        db.query(Medicamento).join(PessoaTEA).filter(PessoaTEA.familia_id == familia_id).all()
    )
    total_medicamentos = len(medicamentos_familia)

    agendamentos_familia = (
        db.query(Agenda).join(PessoaTEA).filter(PessoaTEA.familia_id == familia_id).all()
    )
    total_compromissos = len(agendamentos_familia)

    receitas_familia = (
        db.query(ReceitaMedica).join(PessoaTEA).filter(PessoaTEA.familia_id == familia_id).all()
    )
    total_receitas = len(receitas_familia)

    total_notificacoes_nao_lidas = (
        db.query(Notificacao)
        .join(PessoaTEA)
        .filter(PessoaTEA.familia_id == familia_id, Notificacao.lida == False)
        .count()
    )

    medicamentos_criticos = [
        med for med in medicamentos_familia
        if medicamento_service.calcular_status_medicamento(med)["status"] in ["CRÍTICO", "ESGOTADO"]
    ]

    hoje = date.today()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)

    compromissos_hoje = [
        comp for comp in agendamentos_familia if comp.data_hora.date() == hoje
    ]
    compromissos_semana = [
        comp for comp in agendamentos_familia if inicio_semana <= comp.data_hora.date() <= fim_semana
    ]

    receitas_vencendo = [
        rec for rec in receitas_familia
        if receita_service.calcular_status_receita(rec)["status"] in ["ALERTA", "CRÍTICO"]
    ]

    receitas_vencidas = [
        rec for rec in receitas_familia
        if receita_service.calcular_status_receita(rec)["status"] == "VENCIDA"
    ]

    return {
        "total_pessoas_tea": total_pessoas_tea,
        "total_medicamentos": total_medicamentos,
        "total_notificacoes_nao_lidas": total_notificacoes_nao_lidas,
        "total_receitas": total_receitas,
        "total_compromissos": total_compromissos,
        "medicamentos_criticos": medicamentos_criticos,
        "receitas_vencendo": receitas_vencendo,
        "receitas_vencidas": receitas_vencidas,
        "compromissos_hoje": compromissos_hoje,
        "compromissos_semana": compromissos_semana,
    }