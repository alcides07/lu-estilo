from fastapi import APIRouter, Depends, Path
from uuid import UUID
from models.client import Client
from permissions.order import check_owner_order_permission
from filters.order import OrderFilter
from permissions.utils.client_owner_or_admin import (
    owner_permission_or_admin,
)
from permissions.administrator import is_administrator
from schemas.order_product import OrderProductRead
from permissions.client import is_client
from schemas.utils.pagination import PaginationSchema
from schemas.utils.responses import ResponsePagination, ResponseUnit
from services.order import OrderService
from schemas.order import OrderCreate, OrderRead, OrderUpdate
from dependencies.get_user_authenticated import get_user_authenticated
from dependencies.get_session_db import SessionDep
from models.user import User


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(get_user_authenticated)],
)


@router.get(
    "/",
    dependencies=[Depends(is_administrator)],
)
async def list(
    session: SessionDep,
    pagination: PaginationSchema = Depends(),
    filters: OrderFilter = Depends(),
) -> ResponsePagination[OrderProductRead]:

    service = OrderService(session)
    orders, metadata = await service.list_orders(pagination, filters)

    return ResponsePagination(data=orders, metadata=metadata)


@router.get(
    "/{id}/",
)
async def read(
    session: SessionDep,
    id: UUID = Path(description="Identificador do pedido"),
    _: Client = Depends(owner_permission_or_admin(check_owner_order_permission)),
) -> ResponseUnit[OrderProductRead]:
    service = OrderService(session)
    order = await service.read_order(id)

    return ResponseUnit(data=order)


@router.post("/", status_code=201, dependencies=[Depends(is_client)])
async def create(
    order: OrderCreate,
    session: SessionDep,
    current_user: User = Depends(get_user_authenticated),
) -> OrderProductRead:

    service = OrderService(session)
    return await service.create_order(order=order, user=current_user)


@router.put(
    "/{id}/",
    dependencies=[Depends(is_administrator)],
)
async def update(
    order: OrderUpdate,
    session: SessionDep,
    id: UUID = Path(description="Identificador do pedido"),
) -> ResponseUnit[OrderRead]:
    service = OrderService(session)
    data = await service.update_order(id, order)
    return ResponseUnit(data=data)


@router.delete(
    "/{id}/",
    status_code=204,
    dependencies=[Depends(is_administrator)],
)
async def delete(
    session: SessionDep,
    id: UUID = Path(description="Identificador do pedido"),
):
    service = OrderService(session)
    data = await service.delete_order(id)
    return ResponseUnit(data=data)
