from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product_model import Produto
from app.models.user_model import User
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)

    def create_product(self, data: ProductCreate, user: User) -> Produto:
        product = Produto(
            nome=data.nome.strip(),
            categoria=data.categoria.strip(),
            quantidade=data.quantidade,
            peso=data.peso,
            preco=data.preco,
            criado_por_id=user.id,
        )
        return self.repository.create(product)

    def list_products(
        self,
        nome: str | None = None,
        categoria: str | None = None,
        estoque_baixo: bool | None = None,
    ) -> list[Produto]:
        return self.repository.list(nome=nome, categoria=categoria, estoque_baixo=estoque_baixo)

    def get_product(self, product_id: int) -> Produto:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
        return product

    def update_product(self, product_id: int, data: ProductUpdate) -> Produto:
        product = self.get_product(product_id)
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum campo enviado para atualização")
        return self.repository.update(product, update_data)

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        self.repository.delete(product)
