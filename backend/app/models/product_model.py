from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(160), nullable=False, index=True)
    categoria = Column(String(120), nullable=False, index=True)
    quantidade = Column(Integer, nullable=False, default=0)
    peso = Column(Float, nullable=False, default=0.0)
    preco = Column(Float, nullable=False, default=0.0)
    criado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    criador = relationship("User", back_populates="produtos")
    movimentacoes = relationship("MovimentoEstoque", back_populates="produto", cascade="all, delete-orphan")
