from fastapi import APIRouter, Depends
from dependencies.get_user_authenticated import get_user_authenticated
from dependencies.get_session_db import SessionDep
from filters.category import CategoryFilter
from permissions.administrator import is_administrator
from schemas.category import CategoryCreate, CategoryRead
from schemas.utils.pagination import PaginationSchema
from schemas.utils.responses import ResponsePagination
from services.category import CategoryService


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.get(
    "/",
)
async def list(
    session: SessionDep,
    pagination: PaginationSchema = Depends(),
    filters: CategoryFilter = Depends(),
) -> ResponsePagination[CategoryRead]:

    service = CategoryService(session)
    data = service.list_categories(pagination=pagination, filters=filters)
    return ResponsePagination(data=data)


@router.post(
    "/",
    status_code=201,
    dependencies=[Depends(is_administrator), Depends(get_user_authenticated)],
)
async def create(
    category: CategoryCreate,
    session: SessionDep,
) -> CategoryRead:
    service = CategoryService(session)
    return service.create_category(category=category)
