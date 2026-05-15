from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.stock_movement_model import MovimentoEstoque
from app.models.user_model import User
from app.repositories.product_repository import ProductRepository
from app.repositories.stock_repository import StockRepository
from app.schemas.stock_schema import StockMovementCreate


class StockService:
    def __init__(self, db: Session):
        self.db = db
        self.product_repository = ProductRepository(db)
        self.stock_repository = StockRepository(db)

    def entrada(self, data: StockMovementCreate, user: User) -> MovimentoEstoque:
        product = self.product_repository.get_by_id(data.produto_id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

        product.quantidade += data.quantidade
        movement = MovimentoEstoque(
            produto_id=product.id,
            usuario_id=user.id,
            tipo="entrada",
            quantidade=data.quantidade,
            observacao=data.observacao,
        )
        self.db.add(movement)
        self.db.commit()
        self.db.refresh(product)
        self.db.refresh(movement)
        return movement

    def saida(self, data: StockMovementCreate, user: User) -> MovimentoEstoque:
        product = self.product_repository.get_by_id(data.produto_id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

        if product.quantidade < data.quantidade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantidade insuficiente em estoque",
            )

        product.quantidade -= data.quantidade
        movement = MovimentoEstoque(
            produto_id=product.id,
            usuario_id=user.id,
            tipo="saida",
            quantidade=data.quantidade,
            observacao=data.observacao,
        )
        self.db.add(movement)
        self.db.commit()
        self.db.refresh(product)
        self.db.refresh(movement)
        return movement

    def list_movements(self, produto_id: int | None = None) -> list[MovimentoEstoque]:
        return self.stock_repository.list_movements(produto_id=produto_id)
