from typing import Any
from fastapi import APIRouter, Depends, Path
from uuid import UUID
from schemas.order_product import OrderProductRead
from permissions.client import is_client
from schemas.utils.pagination import PaginationSchema
from schemas.utils.responses import ResponsePagination, ResponseUnit
from services.order import OrderService
from schemas.order import OrderCreate
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
    # dependencies=[Depends(is_administrator)],
)
async def list(
    session: SessionDep,
    pagination: PaginationSchema = Depends(),
    # filters: ClientFilter = Depends(),
) -> ResponsePagination[OrderProductRead]:

    service = OrderService(session)
    orders = await service.list_orders()

    return ResponsePagination(data=orders)


@router.get(
    "/{id}/",
)
async def read(
    session: SessionDep,
    id: UUID = Path(),
    # _: Client = Depends(check_owner_order_permission),
) -> Any:
    service = OrderService(session)
    order = await service.list_orders()

    return ResponseUnit(data=order)
    # return order_to_read_model(order)
    # data = read_client(session=session, client_id=id)


# @router.get("/orders/{order_id}", response_model=OrderRead)
# async def read_order(order_id: UUID, session: AsyncSession = Depends(get_db)):
#     order = await get_order_with_products(session, order_id)
#     return order_to_read_model(order)


@router.post("/", status_code=201, dependencies=[Depends(is_client)])
async def create(
    order: OrderCreate,
    session: SessionDep,
    current_user: User = Depends(get_user_authenticated),
) -> OrderProductRead:

    service = OrderService(session)
    return await service.create_order(order=order, user=current_user)


# @router.put("/{id}/")
# async def update(
#     client: ClientUpdate,
#     session: SessionDep,
#     id: int = Path(description="Identificador do cliente"),
#     _: Client = Depends(check_owner_client_permission),
# ) -> ClientRead:
#     data = update_client(client, id, session)
#     return data


# @router.delete("/{id}/", status_code=204)
# async def delete(
#     session: SessionDep,
#     id: int = Path(description="Identificador do cliente"),
#     _: Client = Depends(check_owner_client_permission),
# ):
#     await delete_client(id, session)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
