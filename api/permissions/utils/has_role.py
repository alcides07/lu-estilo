import jwt
from fastapi import HTTPException, status
from api.schemas.role import Role
from decouple import config
from api.core.security.auth import ALGORITHM

SECRET_KEY = config("SECRET_KEY")


def has_role(token: str, role: Role) -> bool:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    roles = payload.get("roles", [])

    if role in roles:
        return True

    raise HTTPException(status.HTTP_403_FORBIDDEN)
