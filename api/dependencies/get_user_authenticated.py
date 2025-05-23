from sqlalchemy import select
from api.dependencies.get_session_db import SessionDep
from api.models.user import User
from decouple import config
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from api.schemas.auth import TokenType
from api.services.auth import verify_token


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


async def get_user_authenticated(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User:
    payload = await verify_token(token, TokenType.ACCESS)
    sub = payload.sub

    user = session.execute(select(User).where(User.name == sub)).scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
