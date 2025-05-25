from fastapi import APIRouter, Depends
from services.administrator import AdministratorService
from dependencies.get_session_db import SessionDep
from filters.administrator import AdministratorFilter
from models.user import User
from permissions.administrator import is_administrator
from permissions.user import check_ower_user_permission
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

    service = AdministratorService(session)
    data, metadata = service.list_administrators(pagination=pagination, filters=filters)
    return ResponsePagination(data=data, metadata=metadata)


@router.post("/", response_model=AdministratorRead, status_code=201)
async def create(
    administrator: AdministratorCreate,
    session: SessionDep,
    current_user: User = Depends(get_user_authenticated),
):
    await check_ower_user_permission(administrator.user_id, current_user)

    service = AdministratorService(session)
    return service.create_administrator(administrator)
