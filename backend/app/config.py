import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    """Configurações centrais do sistema.

    O uso de @lru_cache em get_settings aplica um Singleton simples:
    a aplicação reaproveita a mesma instância de configuração durante a execução.
    """

    app_name: str = os.getenv("APP_NAME", "StockFlow API")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./estoque.db")
    secret_key: str = os.getenv("SECRET_KEY", "stockflow-chave-dev-altere-em-producao")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
