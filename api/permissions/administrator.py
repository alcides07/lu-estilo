from typing import Annotated
from fastapi import Depends
from api.permissions.utils.has_role import has_role
from api.schemas.role import Role
from api.core.security.auth import oauth2_scheme


async def is_administrator(token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    return await has_role(token, Role.ADMINISTRATOR)
