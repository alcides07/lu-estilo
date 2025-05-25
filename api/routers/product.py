from fastapi import APIRouter, Depends, Path, Response, status
from dependencies.get_user_authenticated import get_user_authenticated
from dependencies.get_session_db import SessionDep
from filters.product import ProductFilter
from permissions.administrator import is_administrator
from schemas.product import ProductCreate, ProductRead, ProductUpdate
from schemas.utils.pagination import PaginationSchema
from schemas.utils.responses import ResponsePagination, ResponseUnit
from services.product import ProductService


router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/")
async def list(
    session: SessionDep,
    pagination: PaginationSchema = Depends(),
    filters: ProductFilter = Depends(),
) -> ResponsePagination[ProductRead]:

    service = ProductService(session)
    data, metadata = service.list_products(pagination=pagination, filters=filters)
    return ResponsePagination(data=data, metadata=metadata)


@router.get(
    "/{id}/",
)
async def read(
    session: SessionDep,
    id: int = Path(description="Identificador do produto"),
) -> ResponseUnit[ProductRead]:

    service = ProductService(session)
    data = await service.read_product(id)
    return ResponseUnit(data=data)


@router.post(
    "/",
    status_code=201,
    dependencies=[Depends(is_administrator), Depends(get_user_authenticated)],
)
async def create(
    product: ProductCreate,
    session: SessionDep,
) -> ProductRead:
    service = ProductService(session)
    return service.create_product(product=product)


@router.put(
    "/{id}/",
    dependencies=[Depends(is_administrator), Depends(get_user_authenticated)],
)
async def update(
    product: ProductUpdate,
    session: SessionDep,
    id: int = Path(description="Identificador do produto"),
) -> ProductRead:
    service = ProductService(session)
    data = service.update_product(id, product)
    return data


@router.delete(
    "/{id}/",
    status_code=204,
    dependencies=[Depends(is_administrator), Depends(get_user_authenticated)],
)
async def delete(
    session: SessionDep,
    id: int = Path(description="Identificador do produto"),
):
    service = ProductService(session)
    await service.delete_product(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
