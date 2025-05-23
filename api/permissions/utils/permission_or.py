from fastapi import HTTPException, Depends
from typing import Callable, Awaitable
from api.dependencies.get_user_authenticated import get_user_authenticated
from api.models.user import User


def check_permissions_or(*permission_checks: Callable[[User], Awaitable[bool]]):
    """
    Verifica se pelo menos UMA das permissões é válida (OR lógico).
    """

    async def wrapper(
        user: User = Depends(get_user_authenticated),
    ):
        exceptions = []

        for check in permission_checks:
            try:
                result = await check(user)
                if result:
                    return True
            except HTTPException as e:
                exceptions.append(e)

        if exceptions:
            raise exceptions[0]
        raise HTTPException(status_code=403, detail="Acesso negado")

    return Depends(wrapper)
