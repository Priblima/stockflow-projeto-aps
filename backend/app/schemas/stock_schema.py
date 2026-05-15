from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StockMovementCreate(BaseModel):
    produto_id: int = Field(..., ge=1)
    quantidade: int = Field(..., ge=1)
    observacao: Optional[str] = Field(None, max_length=255)


class StockMovementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    produto_id: int
    usuario_id: Optional[int] = None
    tipo: str
    quantidade: int
    observacao: Optional[str] = None
    criado_em: datetime
