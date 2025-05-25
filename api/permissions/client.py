from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dependencies.get_user_authenticated import get_user_authenticated
from models.client import Client
from models.user import User
from permissions.utils.has_role import has_role
from schemas.role import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


async def is_client(token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    return await has_role(token, Role.CLIENT)


async def check_owner_client_permission(
    id: int, current_user: User = Depends(get_user_authenticated)
) -> Client:
    if current_user.client and current_user.client.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return current_user.client
