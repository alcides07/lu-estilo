from fastapi import APIRouter, Depends
from dependencies.get_session_db import SessionDep
from filters.administrator import AdministratorFilter
from models.user import User
from orm.administrator import create_administrator, list_administrators
from permissions.administrator import is_administrator
from permissions.utils.check_owner_permission import check_ower_user_permission
from schemas.administrator import AdministratorCreate, AdministratorRead
from dependencies.get_user_authenticated import get_user_authenticated
from schemas.utils.pagination import PaginationSchema
from schemas.utils.responses import ResponsePagination


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
