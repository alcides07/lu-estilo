from typing import Annotated
from fastapi import APIRouter, Depends
from services.user import UserService
from dependencies.get_session_db import SessionDep
from schemas.auth import (
    LoginOut,
    TokenDataToSubmitToStorage,
    TokenRefreshOut,
    TokenType,
)
from fastapi.security import OAuth2PasswordRequestForm

from schemas.user import UserCreate, UserRead
from schemas.utils.get_roles_from_user import get_roles_from_user
from services.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register/", status_code=201)
async def create(user: UserCreate, session: SessionDep) -> UserRead:

    service = UserService(session)
    return service.create_user(user)


@router.post("/login/")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> LoginOut:
    user = authenticate_user(session, form_data.username, form_data.password)
    data_token = TokenDataToSubmitToStorage(
        sub=user.name,
        user_id=user.id,
        roles=get_roles_from_user(user),
    )

    access_token = await create_access_token(data_token)
    refresh_token = await create_refresh_token(data_token)

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
