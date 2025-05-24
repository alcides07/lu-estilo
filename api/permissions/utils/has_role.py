from fastapi import HTTPException, status
from api.schemas.role import Role
from api.schemas.auth import TokenType
from decouple import config
from api.services.auth import verify_token

SECRET_KEY = config("SECRET_KEY")


async def has_role(token: str, role: Role) -> bool:
    payload = await verify_token(token, TokenType.ACCESS)

    if role in payload.roles:
        return True

    raise HTTPException(status.HTTP_403_FORBIDDEN)
