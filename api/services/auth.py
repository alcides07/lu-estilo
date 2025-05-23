import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import select
from api.models.user import User
from decouple import config
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from api.schemas.auth import TokenDataToSubmitToStorage, TokenStorage, TokenType
from api.core.security.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
)

SECRET_KEY = config("SECRET_KEY")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(session: Session, credential: str, password: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = session.execute(
        select(User).where(User.name == credential)
    ).scalar_one_or_none()
    if not user:
        raise credentials_exception
    if not verify_password(password, user.password):
        raise credentials_exception
    return user


async def verify_token(token: str, expected_token_type: TokenType) -> TokenStorage:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        token_type = payload.get("token_type")

        if sub is None or token_type != expected_token_type:
            raise credentials_exception

        return TokenStorage(**payload)

    except ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expirado")

    except InvalidTokenError:
        raise credentials_exception


def build_token_payload(
    data: TokenDataToSubmitToStorage,
    expires_delta: timedelta,
    token_type: TokenType,
) -> Dict[str, Any]:
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        **data.model_dump(),
        "exp": expire,
        "token_type": token_type,
    }
    return payload


async def create_access_token(data: TokenDataToSubmitToStorage):
    payload = build_token_payload(
        data=data,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type=TokenType.ACCESS,
    )
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def create_refresh_token(data: TokenDataToSubmitToStorage) -> str:
    payload = build_token_payload(
        data=data,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        token_type=TokenType.REFRESH,
    )
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
