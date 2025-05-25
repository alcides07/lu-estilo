from uuid import UUID
from fastapi import Depends, HTTPException, status
from models.client import Client
from dependencies.get_session_db import SessionDep
from models.order import Order
from orm.utils.get_object_or_404 import get_object_or_404
from dependencies.get_user_authenticated import get_user_authenticated
from models.user import User


async def check_owner_order_permission(
    id: UUID,
    session: SessionDep,
    current_user: User = Depends(get_user_authenticated),
) -> Client:
    error = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
    )
    if current_user.client:
        order = get_object_or_404(session, Order, id)
        if order.client_id != current_user.client.id:
            raise error

        return current_user.client

    raise error
