from passlib.context import CryptContext
from sqlalchemy.orm import Session
from api.dependencies.get_session_db import get_session_db
from api.models.user import User
from jwt.exceptions import InvalidTokenError
from decouple import config
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from api.orm.utils.exists import exists
from api.schemas.auth import TokenType
from api.services.auth import verify_token


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user_authenticated(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = await verify_token(token, TokenType.ACCESS)
        username = payload.sub

    except InvalidTokenError:
        raise credentials_exception

    user = exists(session, User, username=username)
    if user is None:
        raise credentials_exception

    return user
