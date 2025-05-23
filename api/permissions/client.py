from fastapi import HTTPException, status
from api.models.user import User


async def is_client(
    user: User,
):
    if user.client:
        return True
    raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Acesso negado")
