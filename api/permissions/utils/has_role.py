from fastapi import HTTPException, status
from schemas.role import Role
from schemas.auth import TokenType
from decouple import config
from services.auth import verify_token

SECRET_KEY = config("SECRET_KEY")


async def has_role(token: str, role: Role) -> bool:
    payload = await verify_token(token, TokenType.ACCESS)

    if role in payload.roles:
        return True

    raise HTTPException(status.HTTP_403_FORBIDDEN)
