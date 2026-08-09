from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.models import Agenda, Medicamento, Notificacao, PessoaTEA, ReceitaMedica, StatusAgendamento, Usuario
from backend.services import medicamento_service, receita_service


def _criar_notificacao_se_nao_existir(
    db: Session, pessoa_tea: PessoaTEA, titulo: str, mensagem: str, buffer: list
):
    """
    Helper para criar uma notificação apenas se uma com o mesmo título para a mesma pessoa não existir e não estiver lida.
    Isso evita notificações duplicadas para o mesmo problema.
    """
    existe = (
        db.query(Notificacao)
        .filter(
            Notificacao.pessoa_tea_id == pessoa_tea.id,
            Notificacao.titulo == titulo,
            Notificacao.lida == False,
        )
        .first()
    )

    if not existe:
        nova_notificacao = Notificacao(
            pessoa_tea_id=pessoa_tea.id,
            titulo=titulo,
            mensagem=mensagem,
            data_envio=datetime.now(timezone.utc),
        )
        buffer.append(nova_notificacao)


def _gerar_notificacoes_medicamentos(db: Session, buffer: list):
    """
    Varre todos os medicamentos e gera notificações de estoque.
    """
    medicamentos = db.query(Medicamento).all()
    for med in medicamentos:
        status_info = medicamento_service.calcular_status_medicamento(med)
        dias_restantes = status_info["dias_restantes"]

        if status_info["status"] == "CRÍTICO":
            titulo = f"Estoque Crítico: {med.nome}"
            mensagem = f"O medicamento {med.nome} para {med.pessoa_tea.nome} atingiu o estoque mínimo. Restam {med.quantidade_atual} unidades."
            _criar_notificacao_se_nao_existir(db, med.pessoa_tea, titulo, mensagem, buffer)

        if dias_restantes is not None and dias_restantes <= 3:
            titulo = f"Urgente: {med.nome} acabará em {dias_restantes} dias"
            mensagem = f"O medicamento {med.nome} para {med.pessoa_tea.nome} está prestes a acabar. Apenas {dias_restantes} dias restantes."
            _criar_notificacao_se_nao_existir(db, med.pessoa_tea, titulo, mensagem, buffer)

        elif dias_restantes is not None and dias_restantes <= 7:
            titulo = f"Atenção: {med.nome} acabará em breve"
            mensagem = f"O medicamento {med.nome} para {med.pessoa_tea.nome} tem estoque para apenas {dias_restantes} dias."
            _criar_notificacao_se_nao_existir(db, med.pessoa_tea, titulo, mensagem, buffer)

def _gerar_notificacoes_receitas(db: Session, buffer: list):
    """
    Varre todas as receitas e gera notificações de validade.
    """
    receitas = db.query(ReceitaMedica).all()
    for rec in receitas:
        status_info = receita_service.calcular_status_receita(rec)
        status = status_info["status"]
        dias = status_info["dias_para_vencer"]

        if status == "VENCIDA":
            titulo = f"Receita Vencida: {rec.medicamento.nome}"
            mensagem = f"A receita de {rec.medicamento.nome} para {rec.pessoa_tea.nome} venceu há {-dias} dias."
            _criar_notificacao_se_nao_existir(db, rec.pessoa_tea, titulo, mensagem, buffer)
        elif status == "CRÍTICO":
            titulo = f"Receita Vencendo: {rec.medicamento.nome}"
            mensagem = f"A receita de {rec.medicamento.nome} para {rec.pessoa_tea.nome} vence em {dias} dias. Renove com urgência."
            _criar_notificacao_se_nao_existir(db, rec.pessoa_tea, titulo, mensagem, buffer)
        elif status == "ALERTA":
            titulo = f"Alerta de Validade: {rec.medicamento.nome}"
            mensagem = f"A receita de {rec.medicamento.nome} para {rec.pessoa_tea.nome} vence em {dias} dias."
            _criar_notificacao_se_nao_existir(db, rec.pessoa_tea, titulo, mensagem, buffer)

def _gerar_notificacoes_agenda(db: Session, buffer: list):
    """
    Varre todos os compromissos e gera notificações de proximidade.
    """
    agora = datetime.now(timezone.utc)
    amanha = agora + timedelta(days=1)
    duas_horas = agora + timedelta(hours=2)

    # Busca compromissos que ainda não foram realizados
    compromissos = db.query(Agenda).filter(Agenda.status == StatusAgendamento.agendado).all()

    for comp in compromissos:
        # Converte para UTC se for naive
        data_hora_compromisso = comp.data_hora.replace(tzinfo=None) if comp.data_hora.tzinfo else comp.data_hora

        # Regra 1: Compromisso vencido (passou e não foi marcado como realizado/cancelado)
        if data_hora_compromisso < agora:
            titulo = f"Compromisso Vencido: {comp.titulo}"
            mensagem = f"O compromisso '{comp.titulo}' para {comp.pessoa_tea.nome} em {data_hora_compromisso.strftime('%d/%m/%Y %H:%M')} não foi atualizado. Ele já ocorreu?"
            _criar_notificacao_se_nao_existir(db, comp.pessoa_tea, titulo, mensagem, buffer)

        # Regra 2: Compromisso em 2 horas
        elif agora < data_hora_compromisso <= duas_horas:
            titulo = f"Lembrete: {comp.titulo} em breve"
            mensagem = f"O compromisso '{comp.titulo}' para {comp.pessoa_tea.nome} é hoje às {data_hora_compromisso.strftime('%H:%M')}."
            _criar_notificacao_se_nao_existir(db, comp.pessoa_tea, titulo, mensagem, buffer)

        # Regra 3: Compromisso amanhã
        elif agora < data_hora_compromisso <= amanha:
            titulo = f"Lembrete: {comp.titulo} amanhã"
            mensagem = f"Lembrete do compromisso '{comp.titulo}' para {comp.pessoa_tea.nome} amanhã, dia {data_hora_compromisso.strftime('%d/%m')} às {data_hora_compromisso.strftime('%H:%M')}."
            _criar_notificacao_se_nao_existir(db, comp.pessoa_tea, titulo, mensagem, buffer)

def gerar_notificacoes_automaticas(db: Session):
    """
    Ponto central para gerar todas as notificações automáticas do sistema.
    Em um sistema real, isso seria executado por um worker em background (ex: Celery, ARQ).
    """
    novas_notificacoes = []
    _gerar_notificacoes_medicamentos(db, novas_notificacoes)
    _gerar_notificacoes_receitas(db, novas_notificacoes)
    _gerar_notificacoes_agenda(db, novas_notificacoes)

    if novas_notificacoes:
        db.add_all(novas_notificacoes)
        db.commit()

    return {"novas_notificacoes_criadas": len(novas_notificacoes)}


def get_notificacao_e_verificar_permissao(
    db: Session, notificacao_id: int, current_user: Usuario
) -> Notificacao:
    """Busca uma notificação e verifica se o usuário tem permissão para acessá-la."""
    notificacao = (
        db.query(Notificacao)
        .join(PessoaTEA)
        .filter(
            Notificacao.id == notificacao_id,
            PessoaTEA.familia_id == current_user.familia_id,
        )
        .first()
    )
    if not notificacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notificação não encontrada"
        )
    return notificacao


def get_notificacoes_da_familia(db: Session, current_user: Usuario) -> List[Notificacao]:
    """Retorna todas as notificações (não lidas e lidas) da família do usuário."""
    return (
        db.query(Notificacao)
        .join(PessoaTEA)
        .filter(PessoaTEA.familia_id == current_user.familia_id)
        .order_by(Notificacao.lida.asc(), Notificacao.data_envio.desc())
        .all()
    )


def marcar_como_lida(
    db: Session, notificacao_id: int, current_user: Usuario
) -> Notificacao:
    """Marca uma notificação como lida."""
    notificacao = get_notificacao_e_verificar_permissao(db, notificacao_id, current_user)
    notificacao.lida = True
    db.commit()
    db.refresh(notificacao)
    return notificacao