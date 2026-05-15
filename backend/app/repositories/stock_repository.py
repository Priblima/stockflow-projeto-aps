from sqlalchemy.orm import Session

from app.models.stock_movement_model import MovimentoEstoque


class StockRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_movement(self, movement: MovimentoEstoque) -> MovimentoEstoque:
        self.db.add(movement)
        self.db.commit()
        self.db.refresh(movement)
        return movement

    def list_movements(self, produto_id: int | None = None) -> list[MovimentoEstoque]:
        query = self.db.query(MovimentoEstoque)
        if produto_id is not None:
            query = query.filter(MovimentoEstoque.produto_id == produto_id)
        return query.order_by(MovimentoEstoque.id.desc()).all()
