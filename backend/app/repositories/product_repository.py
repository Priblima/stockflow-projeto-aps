from sqlalchemy.orm import Session

from app.models.product_model import Produto


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, product: Produto) -> Produto:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def list(
        self,
        nome: str | None = None,
        categoria: str | None = None,
        estoque_baixo: bool | None = None,
        limite_estoque_baixo: int = 5,
    ) -> list[Produto]:
        query = self.db.query(Produto)
        if nome:
            query = query.filter(Produto.nome.ilike(f"%{nome}%"))
        if categoria:
            query = query.filter(Produto.categoria.ilike(f"%{categoria}%"))
        if estoque_baixo is True:
            query = query.filter(Produto.quantidade <= limite_estoque_baixo)
        return query.order_by(Produto.id.desc()).all()

    def get_by_id(self, product_id: int) -> Produto | None:
        return self.db.query(Produto).filter(Produto.id == product_id).first()

    def update(self, product: Produto, data: dict) -> Produto:
        for field, value in data.items():
            setattr(product, field, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Produto) -> None:
        self.db.delete(product)
        self.db.commit()
