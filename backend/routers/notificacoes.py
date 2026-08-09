from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database import get_db
from backend.models import Usuario
from backend.schemas.notificacao import NotificacaoPublic
from backend.services import notificacao_service

router = APIRouter(tags=["Notificações"])


@router.post("/verificar-medicamentos", status_code=status.HTTP_200_OK)
def trigger_medication_check(db: Session = Depends(get_db)):
    """
    Endpoint administrativo para acionar manualmente a verificação de medicamentos e geração de notificações.
    Em produção, isso seria um processo em background.
    """
    return notificacao_service.gerar_notificacoes_automaticas(db)


@router.get("/", response_model=List[NotificacaoPublic])
def get_notificacoes_da_familia(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Lista todas as notificações da família do usuário, ordenadas por não lidas primeiro."""
    return notificacao_service.get_notificacoes_da_familia(db, current_user)


@router.get("/{notificacao_id}", response_model=NotificacaoPublic)
def get_notificacao(
    notificacao_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Busca uma notificação específica pelo ID."""
    return notificacao_service.get_notificacao_e_verificar_permissao(
        db, notificacao_id, current_user
    )


@router.patch("/{notificacao_id}/marcar-lida", response_model=NotificacaoPublic)
def mark_notification_as_read(
    notificacao_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Marca uma notificação como lida."""
    return notificacao_service.marcar_como_lida(db, notificacao_id, current_user)


@router.delete("/{notificacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notificacao_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Deleta uma notificação."""
    notificacao = notificacao_service.get_notificacao_e_verificar_permissao(
        db, notificacao_id, current_user
    )
    db.delete(notificacao)
    db.commit()