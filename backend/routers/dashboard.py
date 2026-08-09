from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database import get_db
from backend.models import Usuario
from backend.schemas.dashboard import DashboardStats
from backend.services import dashboard_service

router = APIRouter(tags=["Dashboard"])


@router.get("/", response_model=DashboardStats)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Retorna um resumo com os principais indicadores da família."""
    return dashboard_service.get_dashboard_stats(db, current_user)