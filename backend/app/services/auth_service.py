from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import LoginRequest


class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def login(self, credentials: LoginRequest) -> str:
        user = self.repository.get_by_email(credentials.email)
        if user is None or not verify_password(credentials.senha, user.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos",
            )
        if not user.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo",
            )
        return create_access_token(subject=user.email)
