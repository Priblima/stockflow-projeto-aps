from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=160)
    categoria: str = Field(..., min_length=2, max_length=120)
    quantidade: int = Field(..., ge=0)
    peso: float = Field(..., ge=0)
    preco: float = Field(..., ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=160)
    categoria: Optional[str] = Field(None, min_length=2, max_length=120)
    quantidade: Optional[int] = Field(None, ge=0)
    peso: Optional[float] = Field(None, ge=0)
    preco: Optional[float] = Field(None, ge=0)


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    criado_por_id: Optional[int] = None
    criado_em: datetime
    atualizado_em: datetime
