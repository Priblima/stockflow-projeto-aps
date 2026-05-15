from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user_model import User
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProductService(db).create_product(data, current_user)


@router.get("", response_model=list[ProductResponse])
def listar_produtos(
    nome: str | None = Query(None, description="Filtro por nome"),
    categoria: str | None = Query(None, description="Filtro por categoria"),
    estoque_baixo: bool | None = Query(None, description="Filtrar produtos com quantidade <= 5"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProductService(db).list_products(nome=nome, categoria=categoria, estoque_baixo=estoque_baixo)


@router.get("/{produto_id}", response_model=ProductResponse)
def obter_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProductService(db).get_product(produto_id)


@router.put("/{produto_id}", response_model=ProductResponse)
def atualizar_produto(
    produto_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProductService(db).update_product(produto_id, data)


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ProductService(db).delete_product(produto_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
