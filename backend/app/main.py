from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.models import MovimentoEstoque, Produto, User  # noqa: F401 - garante registro dos models
from app.routes import auth_routes, product_routes, report_routes, stock_routes

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="API REST do StockFlow — Sistema de Controle de Estoque com FastAPI, SQLite, SQLAlchemy e JWT.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(product_routes.router)
app.include_router(stock_routes.router)
app.include_router(report_routes.router)


@app.get("/", tags=["Health Check"])
def home():
    return {"mensagem": "StockFlow API funcionando"}


@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}
