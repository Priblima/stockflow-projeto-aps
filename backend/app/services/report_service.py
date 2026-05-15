from sqlalchemy.orm import Session

from app.models.product_model import Produto
from app.models.stock_movement_model import MovimentoEstoque


class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def resumo_estoque(self) -> dict:
        produtos = self.db.query(Produto).all()
        movimentacoes = self.db.query(MovimentoEstoque).all()
        total_produtos = len(produtos)
        quantidade_total = sum(produto.quantidade for produto in produtos)
        valor_total = sum(produto.quantidade * produto.preco for produto in produtos)
        baixo_estoque = [produto for produto in produtos if produto.quantidade <= 5]

        return {
            "total_produtos": total_produtos,
            "quantidade_total_itens": quantidade_total,
            "valor_total_estoque": round(valor_total, 2),
            "produtos_estoque_baixo": len(baixo_estoque),
            "total_movimentacoes": len(movimentacoes),
        }

    def produtos_baixo_estoque(self, limite: int = 5) -> list[Produto]:
        return (
            self.db.query(Produto)
            .filter(Produto.quantidade <= limite)
            .order_by(Produto.quantidade.asc(), Produto.nome.asc())
            .all()
        )
