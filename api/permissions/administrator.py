from typing import Annotated
from fastapi import Depends
from permissions.utils.has_role import has_role
from schemas.role import Role
from core.security.auth import oauth2_scheme


async def is_administrator(token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    return await has_role(token, Role.ADMINISTRATOR)
