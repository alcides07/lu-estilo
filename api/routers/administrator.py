from fastapi import APIRouter, Depends
from api.dependencies.get_session_db import SessionDep
from api.filters.administrator import AdministratorFilter
from api.models.user import User
from api.orm.administrator import create_administrator, list_administrators
from api.permissions.administrator import is_administrator
from api.permissions.utils.check_owner_permission import check_ower_user_permission
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
    dependencies=[Depends(is_administrator)],
)
async def list(
    session: SessionDep,
    pagination: PaginationSchema = Depends(),
    filters: AdministratorFilter = Depends(),
) -> ResponsePagination[AdministratorRead]:

    data = list_administrators(session=session, pagination=pagination, filters=filters)
    return ResponsePagination(data=data)


@router.post("/", response_model=AdministratorRead, status_code=201)
async def create(
    administrator: AdministratorCreate,
    session: SessionDep,
    current_user: User = Depends(get_user_authenticated),
):

    await check_ower_user_permission(administrator.user_id, current_user)

    data = create_administrator(administrator, session)
    return data
