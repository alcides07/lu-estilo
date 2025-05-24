from fastapi import Depends, HTTPException, status
from api.dependencies.get_user_authenticated import get_user_authenticated
from api.models.client import Client
from api.models.user import User


async def check_ower_user_permission(
    id: int, current_user: User = Depends(get_user_authenticated)
):
    if current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return current_user


async def check_owner_client_permission(
    id: int, current_user: User = Depends(get_user_authenticated)
) -> Client:
    if current_user.client and current_user.client.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return current_user.client
