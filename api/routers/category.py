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
    summary="Lista todas as categorias cadastradas",
    description="""
    ## 📝 Listagem de categorias
    Endpoint para consulta de todas as categorias de produtos do sistema com filtragem e paginação dos dados.
    
    ### 🔐 Permissões Necessárias
    - Qualquer usuário (autenticado ou não) pode visualizar as categorias.

    ### 🔎 Parâmetros de Filtro Disponíveis
    - limit       (int): Indica a quantidade de categorias que deseja visualizar
    - offset      (int): Indica a partir de qual categoria da lista deseja visualizar
    - name        (str): Filtra categorias por correspondência parcial do nome
    - description (str): Filtra categorias por correspondência parcial da descrição
    """,
)
async def list(
    session: SessionDep,
    pagination: PaginationSchema = Depends(),
    filters: CategoryFilter = Depends(),
) -> ResponsePagination[CategoryRead]:

    service = CategoryService(session)
    data, metadata = service.list_categories(pagination=pagination, filters=filters)
    return ResponsePagination(data=data, metadata=metadata)


@router.post(
    "/",
    status_code=201,
    dependencies=[Depends(is_administrator), Depends(get_user_authenticated)],
    summary="Lista todas as categorias cadastradas",
    description="""
    ## 📝 Cadastra uma nova categoria
    Endpoint para cadastrar uma nova categoria no sistema.
    
    ### 🔐 Permissões Necessárias
    - É necessário possuir uma conta de **administrador**.

    ### ⬇️ Campos do formulário
    - name        (OBRIGATÓRIO): nome da categoria
    - description (OBRIGATÓRIO): descrição da categoria
    
    ### 🔙 Retorno
    - São retornados os dados cadastrados (name e description), além do identificador "id" da categoria.
    """,
    responses={
        403: {
            "description": "Acesso negado por ser cliente",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
    },
)
async def create(
    category: CategoryCreate,
    session: SessionDep,
) -> CategoryRead:
    service = CategoryService(session)
    return service.create_category(category=category)
