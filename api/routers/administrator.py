from fastapi import APIRouter, Depends
from api.dependencies.get_session_db import SessionDep
from api.filters.administrator import AdministratorFilter
from api.orm.administrator import create_administrator, list_administrators
from api.permissions.administrator import is_administrator
from api.permissions.utils.permission_or import check_permissions_or
from api.schemas.administrator import AdministratorCreate, AdministratorRead
from api.dependencies.get_user_authenticated import get_user_authenticated
from api.schemas.utils.pagination import PaginationSchema
from api.schemas.utils.responses import ResponsePagination


router = APIRouter(
    prefix="/administrators",
    tags=["administrators"],
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
    filters: AdministratorFilter = Depends(),
) -> ResponsePagination[AdministratorRead]:

    data = list_administrators(session=session, pagination=pagination, filters=filters)
    return ResponsePagination(data=data)


@router.post("/", response_model=AdministratorRead, status_code=201)
async def create(administrator: AdministratorCreate, session: SessionDep):
    data = create_administrator(administrator, session)
    return data
