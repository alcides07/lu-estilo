from sqlalchemy import select
from dependencies.get_session_db import SessionDep
from models.user import User
from typing import Annotated
from fastapi import Depends, HTTPException, status
from schemas.auth import TokenType
from services.auth import verify_token
from core.security.auth import oauth2_scheme


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
