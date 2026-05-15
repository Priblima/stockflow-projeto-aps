from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user_model import User
from app.schemas.product_schema import ProductResponse
from app.services.report_service import ReportService

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/resumo")
def resumo_estoque(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService(db).resumo_estoque()


@router.get("/baixo-estoque", response_model=list[ProductResponse])
def produtos_baixo_estoque(
    limite: int = Query(5, ge=0, description="Quantidade limite para considerar estoque baixo"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService(db).produtos_baixo_estoque(limite=limite)
