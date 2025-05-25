from typing import Annotated, Any, Awaitable, Callable
from fastapi import Depends, HTTPException, status
from permissions.administrator import is_administrator
from permissions.client import is_client
from core.security.auth import oauth2_scheme


async def client_owner_or_admin(
    token: str, owner_check_func: Callable[..., Awaitable[Any]]
) -> bool:
    if await is_administrator(token):
        return True

    if await is_client(token):
        return await owner_check_func(token)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
    )


def owner_permission_or_admin(owner_check_func: Callable[..., Awaitable[Any]]):
    async def dependency_wrapper(token: Annotated[str, Depends(oauth2_scheme)]):
        return await client_owner_or_admin(
            token=token, owner_check_func=owner_check_func
        )

    return dependency_wrapper
