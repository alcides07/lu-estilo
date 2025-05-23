from fastapi import HTTPException, status
from api.models.user import User


async def is_administrator(
    user: User,
):
    if user.administrator:
        return True
    raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Acesso negado")
