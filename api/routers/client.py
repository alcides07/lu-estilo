from fastapi import APIRouter, Depends
from api.dependencies.get_user_authenticated import get_user_authenticated
from api.dependencies.get_session_db import SessionDep
from api.filters.client import ClientFilter
from api.orm.client import create_client, list_clients
from api.permissions.administrator import is_administrator
from api.permissions.utils.permission_or import check_permissions_or
from api.schemas.client import ClientCreate, ClientRead
from api.schemas.utils.pagination import PaginationSchema
from api.schemas.utils.responses import ResponsePagination


router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    dependencies=[Depends(get_user_authenticated)],
)


@router.get(
    "/",
    status_code=200,
    dependencies=[check_permissions_or(is_administrator)],
)
async def list(
    session: SessionDep,
    pagination: PaginationSchema = Depends(),
    filters: ClientFilter = Depends(),
) -> ResponsePagination[ClientRead]:

    data = list_clients(session=session, pagination=pagination, filters=filters)
    return ResponsePagination(data=data)


@router.post("/", response_model=ClientRead, status_code=201)
async def create(client: ClientCreate, session: SessionDep):
    data = create_client(client, session)
    return data
