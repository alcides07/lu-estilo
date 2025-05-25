from fastapi import APIRouter, Depends, Path, Response, status
from services.client import ClientService
from dependencies.get_user_authenticated import get_user_authenticated
from dependencies.get_session_db import SessionDep
from filters.client import ClientFilter
from models.client import Client
from models.user import User
from permissions.administrator import is_administrator
from permissions.utils.check_owner_permission import (
    check_owner_client_permission,
    check_ower_user_permission,
)
from schemas.client import ClientCreate, ClientRead, ClientUpdate
from schemas.utils.pagination import PaginationSchema
from schemas.utils.responses import ResponsePagination, ResponseUnit


router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    dependencies=[Depends(get_user_authenticated)],
)


@router.get(
    "/",
    dependencies=[Depends(is_administrator)],
)
async def list(
    session: SessionDep,
    pagination: PaginationSchema = Depends(),
    filters: ClientFilter = Depends(),
) -> ResponsePagination[ClientRead]:

    service = ClientService(session)
    data = service.list_clients(pagination=pagination, filters=filters)
    return ResponsePagination(data=data)


@router.get(
    "/{id}/",
)
async def read(
    session: SessionDep,
    id: int = Path(description="Identificador do cliente"),
    _: Client = Depends(check_owner_client_permission),
) -> ResponseUnit[ClientRead]:

    service = ClientService(session)
    data = await service.read_client(id)
    return ResponseUnit(data=data)


@router.post("/", status_code=201)
async def create(
    client: ClientCreate,
    session: SessionDep,
    current_user: User = Depends(get_user_authenticated),
) -> ClientRead:
    await check_ower_user_permission(client.user_id, current_user)

    service = ClientService(session)
    return service.create_client(client)


@router.put("/{id}/")
async def update(
    client: ClientUpdate,
    session: SessionDep,
    id: int = Path(description="Identificador do cliente"),
    _: Client = Depends(check_owner_client_permission),
) -> ClientRead:
    service = ClientService(session)
    data = service.update_client(client, id)
    return data


@router.delete("/{id}/", status_code=204)
async def delete(
    session: SessionDep,
    id: int = Path(description="Identificador do cliente"),
    _: Client = Depends(check_owner_client_permission),
):
    service = ClientService(session)
    await service.delete_client(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
