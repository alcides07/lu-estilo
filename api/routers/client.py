from fastapi import APIRouter, Depends, Path, Response, status
from api.dependencies.get_user_authenticated import get_user_authenticated
from api.dependencies.get_session_db import SessionDep
from api.filters.client import ClientFilter
from api.models.client import Client
from api.models.user import User
from api.orm.client import (
    create_client,
    list_clients,
    read_client,
    update_client,
    delete_client,
)
from api.permissions.administrator import is_administrator
from api.permissions.utils.check_owner_permission import (
    check_owner_client_permission,
    check_ower_user_permission,
)
from api.schemas.client import ClientCreate, ClientRead, ClientUpdate
from api.schemas.utils.pagination import PaginationSchema
from api.schemas.utils.responses import ResponsePagination, ResponseUnit


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

    data = list_clients(session=session, pagination=pagination, filters=filters)
    return ResponsePagination(data=data)


@router.get(
    "/{id}/",
)
async def read(
    session: SessionDep,
    id: int = Path(description="Identificador do cliente"),
    _: Client = Depends(check_owner_client_permission),
) -> ResponseUnit[ClientRead]:

    data = read_client(session=session, client_id=id)
    return ResponseUnit(data=data)


@router.post("/", status_code=201)
async def create(
    client: ClientCreate,
    session: SessionDep,
    current_user: User = Depends(get_user_authenticated),
) -> ClientRead:
    await check_ower_user_permission(client.user_id, current_user)

    data = create_client(client, session)
    return data


@router.put("/{id}/")
async def update(
    client: ClientUpdate,
    session: SessionDep,
    id: int = Path(description="Identificador do cliente"),
    _: Client = Depends(check_owner_client_permission),
) -> ClientRead:
    data = update_client(client, id, session)
    return data


@router.delete("/{id}/", status_code=204)
async def delete(
    session: SessionDep,
    id: int = Path(description="Identificador do cliente"),
    _: Client = Depends(check_owner_client_permission),
):
    await delete_client(id, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
