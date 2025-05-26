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


@router.get(
    "/",
    summary="Lista todos os produtos cadastrados",
    description="""
    ## 📝 Listagem de produtos
    Endpoint para consulta de todos os produtos do sistema com filtragem e paginação dos dados.
    
    ### 🔐 Permissões Necessárias
    - Os produtos são de visualização pública, assim como não é necessário estar logado.

    ### 🔎 Parâmetros de Filtro Disponíveis
    - limit       (int): Indica a quantidade de produtos que deseja visualizar
    - offset      (int): Indica a partir de qual produto da lista deseja visualizar
    - category_id (int): Filtra produtos de uma categoria específica
    - value__lte  (str): Valor do produto é menor ou igual ao valor informado
    - value__gte  (str): Valor do produto é maior ou igual ao valor informado
    - stock__lte  (str): Estoque é menor ou igual ao estoque informado
    - stock__gte  (str): Estoque é maior ou igual ao estoque informado
    """,
)
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
    summary="Visualiza os dados de um produto específico",
    description="""
    ## 📝 Visualiza os dados de um produto
    Endpoint para visualizar os dados de um produto.
    
    ### 🔐 Permissões Necessárias
    - Os produtos são de visualização pública, assim como não é necessário estar logado.
    
    ### 🔙 Retorno
    - São retornados os dados do produto buscado (id, description, category, bar_code, expiration_date, stock e value)
    """,
    responses={
        404: {
            "description": "Produto não encontrado com identificador informado",
            "content": {
                "application/json": {"example": {"detail": "Produto não encontrado"}}
            },
        },
    },
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
    summary="Cadastra um novo produto",
    description="""
    ## 📝 Cadastra um novo produto
    Endpoint para cadastrar um novo produto no sistema.
    
    ### 🔐 Permissões Necessárias
    - Apenas **administradores** podem cadastrar produtos.

    ### ⬇️ Campos do formulário
    - description  (OBRIGATÓRIO): Descrição do produto
    - value        (OBRIGATÓRIO): Valor do produto
    - bar_code     (OBRIGATÓRIO): Código de barras
    - stock        (OBRIGATÓRIO): Novo estoque do produto
    - expiration_date: Data de validade do produto
    - category_id: Categoria do produto
    
    ### 🔙 Retorno
    - São retornados os dados do produto cadastrado com seus respectivos valores.
    """,
    responses={
        403: {
            "description": "Cliente tentou cadastrar um produto",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": "Administrador submeteu categoria inexistente",
            "content": {
                "application/json": {"example": {"detail": "Categoria não encontrada"}}
            },
        },
    },
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
    summary="Edita dados de um produto específico",
    description="""
    ## 📝 Edita os dados de um produto
    Endpoint para editar os dados de um produto, atualizando-os na base de dados.
    
    ### 🔐 Permissões Necessárias
    - Apenas **administradores** podem editar um produto
    
    ### ⬇️ Campos do formulário
    - description  (OBRIGATÓRIO): Descrição do produto
    - value        (OBRIGATÓRIO): Valor do produto
    - bar_code     (OBRIGATÓRIO): Código de barras
    - stock        (OBRIGATÓRIO): Novo estoque do produto
    - expiration_date: Data de validade do produto
    - category_id: Categoria do produto
    
    ### 🔙 Retorno
    - São retornados os dados do produto após edição (id, description, category, bar_code, expiration_date, stock e value)
    """,
    responses={
        404: {
            "description": "Produto não encontrado com identificador informado",
            "content": {
                "application/json": {"example": {"detail": "Produto não encontrado"}}
            },
        },
        403: {
            "description": "Cliente tentou editar um produto",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
    },
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
    summary="Deleta um produto específico",
    description="""
    ## 📝 Deleta um produto específico
    Endpoint para excluir um produto, removendo os dados da base.
    
    ### 🔐 Permissões Necessárias
    - Apenas **administradores** podem excluir produtos.

    ### 📑 Regras de negócio
    - Um produto que foi inserido em pedidos não pode ser excluído.

    ### 🔙 Retorno
    - Nenhum conteúdo é retornado, apenas o código HTTP 204 indicando um status de sucesso, mas sem conteúdo na resposta.
    """,
    responses={
        400: {
            "description": "Produto vinculado a pedido",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Não é possível excluir o produto pois ele está vinculado a pedidos"
                    }
                }
            },
        },
        404: {
            "description": "Produto não encontrado com o identificador informado",
            "content": {
                "application/json": {"example": {"detail": "Produto não encontrado"}}
            },
        },
    },
)
async def delete(
    session: SessionDep,
    id: int = Path(description="Identificador do produto"),
):
    service = ProductService(session)
    await service.delete_product(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
