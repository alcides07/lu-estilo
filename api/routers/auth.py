from typing import Annotated
from fastapi import APIRouter, Depends
from api.dependencies.get_session_db import SessionDep
from api.orm.user import create_user
from api.schemas.auth import LoginOut, TokenRefreshOut, TokenType
from fastapi.security import OAuth2PasswordRequestForm

from api.schemas.user import UserCreate, UserRead
from api.services.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register/", response_model=UserRead, status_code=201)
async def create(user: UserCreate, session: SessionDep):
    data = create_user(user, session)
    return data


@router.post("/login/")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> LoginOut:
    user = authenticate_user(session, form_data.username, form_data.password)
    access_token = await create_access_token(
        data={"sub": user.name, "user_id": user.id}
    )

    refresh_token = await create_refresh_token(
        data={"sub": user.name, "user_id": user.id}
    )

    return LoginOut(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh-token/")
async def refresh_access_token(
    refresh: str,
) -> TokenRefreshOut:
    user_data = await verify_token(refresh, TokenType.REFRESH)

    new_access_token = await create_access_token(
        data={"sub": user_data.sub, "user_id": user_data.user_id}
    )
    return TokenRefreshOut(access=new_access_token)
