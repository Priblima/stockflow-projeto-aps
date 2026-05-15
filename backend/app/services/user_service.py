from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def register(self, data: UserCreate) -> User:
        existing = self.repository.get_by_email(data.email)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe usuário cadastrado com este e-mail",
            )

        user = User(
            nome=data.nome.strip(),
            email=data.email.strip().lower(),
            senha_hash=hash_password(data.senha),
            perfil="usuario",
            ativo=True,
        )
        return self.repository.create(user)
