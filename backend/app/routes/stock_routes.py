from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user_model import User
from app.schemas.stock_schema import StockMovementCreate, StockMovementResponse
from app.services.stock_service import StockService

router = APIRouter(prefix="/estoque", tags=["Estoque"])


@router.post("/entrada", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED)
def entrada_estoque(
    data: StockMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return StockService(db).entrada(data, current_user)


@router.post("/saida", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED)
def saida_estoque(
    data: StockMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return StockService(db).saida(data, current_user)


@router.get("/movimentacoes", response_model=list[StockMovementResponse])
def listar_movimentacoes(
    produto_id: int | None = Query(None, description="Filtrar por produto"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return StockService(db).list_movements(produto_id=produto_id)
