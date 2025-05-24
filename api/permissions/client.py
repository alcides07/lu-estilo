from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from api.permissions.utils.has_role import has_role
from api.schemas.role import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


async def is_client(token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    return await has_role(token, Role.CLIENT)
