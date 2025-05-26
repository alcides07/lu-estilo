from fastapi import APIRouter, Depends, Path
from uuid import UUID
from models.client import Client
from permissions.order import check_owner_order_permission
from filters.order import OrderFilter
from permissions.utils.client_owner_or_admin import (
    owner_permission_or_admin,
)
from permissions.administrator import is_administrator
from schemas.order_product import OrderProductRead
from permissions.client import is_client
from schemas.utils.pagination import PaginationSchema
from schemas.utils.responses import ResponsePagination, ResponseUnit
from services.order import OrderService
from schemas.order import OrderCreate, OrderRead, OrderUpdate
from dependencies.get_user_authenticated import get_user_authenticated
from dependencies.get_session_db import SessionDep
from models.user import User


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(get_user_authenticated)],
)


@router.get(
    "/",
    dependencies=[Depends(is_administrator)],
    summary="Lista todos os pedidos cadastrados",
    description="""
    ## 📝 Listagem de pedidos
    Endpoint para consulta de todos os pedidos do sistema com filtragem e paginação dos dados.
    
    ### 🔐 Permissões Necessárias
    - Somente **administradores** podem ver todos os pedidos

    ### 🔎 Parâmetros de Filtro Disponíveis
    - limit       (int): Indica a quantidade de pedidos que deseja visualizar
    - offset      (int): Indica a partir de qual pedido da lista deseja visualizar
    - date__lte   (date): Pedidos iguais ou anteriores a uma data
    - date__gte   (date): Pedidos iguais ou posteriores a uma data
    - category_id (int):  Pedidos que possuem produtos da categoria informada
    - status      (OrderStatus): Filtra pedido pelo seu status
    - client_id   (int): Filtra pedidos de uma cliente específico
    """,
)
async def list(
    session: SessionDep,
    pagination: PaginationSchema = Depends(),
    filters: OrderFilter = Depends(),
) -> ResponsePagination[OrderProductRead]:

    service = OrderService(session)
    orders, metadata = await service.list_orders(pagination, filters)

    return ResponsePagination(data=orders, metadata=metadata)


@router.get(
    "/{id}/",
    summary="Visualiza os dados de um pedido específico",
    description="""
    ## 📝 Visualiza os dados de um pedido
    Endpoint para visualizar os dados de um pedido, incluindo a visualização dos produtos.
    
    ### 🔐 Permissões Necessárias
    - Apenas o cliente dono do pedido pode visualizar seu próprio pedido.
    
    ### 🔙 Retorno
    - São retornados os dados do pedido em si, assim como dos produtos contidos nele. Consulte a seção de exemplos de respostas abaixo para mais detalhes.
    """,
)
async def read(
    session: SessionDep,
    id: UUID = Path(description="Identificador do pedido"),
    _: Client = Depends(owner_permission_or_admin(check_owner_order_permission)),
) -> ResponseUnit[OrderProductRead]:
    service = OrderService(session)
    order = await service.read_order(id)

    return ResponseUnit(data=order)


@router.post(
    "/",
    status_code=201,
    dependencies=[Depends(is_client)],
    summary="Cadastra um novo pedido",
    description="""
    ## 📝 Cadastra um novo pedido
    Endpoint para cadastrar um novo pedido no sistema.
    
    ### 🔐 Permissões Necessárias
    - Apenas **clientes** podem cadastrar pedidos, para si próprios.

    ### ⬇️ Campos do formulário
    - products       (OBRIGATÓRIO): Lista de produtos
        - id         (OBRIGATÓRIO): Identificador do produto
        - quantity   (OBRIGATÓRIO): Quantidade desejada do produto
    
    ### 📑 Regras de negócio
        - Um pedido só é aceito se todos os produtos possuírem estoque suficiente para a compra.
    
    ### 🔙 Retorno
    - São retornados os dados do pedido cadastrado, juntamente com os produtos contidos nele.
    """,
    responses={
        404: {
            "description": "Produto(s) não encontrado(s) com identificador(es) informado(s)",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Alguns produtos não foram encontrados: x, y, z"
                    }
                }
            },
        },
        400: {
            "description": "Estoque insuficiente de produto",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "O produto {X} possui {Y} unidades em estoque"
                    }
                }
            },
        },
    },
)
async def create(
    order: OrderCreate,
    session: SessionDep,
    current_user: User = Depends(get_user_authenticated),
) -> OrderProductRead:

    service = OrderService(session)
    return await service.create_order(order=order, user=current_user)


@router.put(
    "/{id}/",
    dependencies=[Depends(is_administrator)],
    summary="Edita os dados de um pedido específico",
    description="""
    ## 📝 Edita os dados de um pedido
    Endpoint para editar os dados de um pedido, atualizando-os na base de dados.
    
    ### 🔐 Permissões Necessárias
    - Apenas **administradores** podem editar um pedido.
    
    ### ⬇️ Campos do formulário
    - status (OBRIGATÓRIO): Status do produto.

    ### 💬 Observações:
    - A edição do pedido ocorre apenas no que diz respeito a atualização do status do pedido, que são eles:
        "Recebido"
        "Aguardando pagamento"
        "Pagamento aprovado"
        "Preparando"
        "Enviado"
        "Saiu para entrega"
        "Entregue"
        "Cancelado"
        "Devolução solicitada"
        "Reembolso solicitado"
        "Devolvido"
        "Reembolsado"

    ### 🔙 Retorno
    - São retornados os dados do pedido após edição.
    """,
    responses={
        404: {
            "description": "Pedido não encontrado com identificador informado",
            "content": {
                "application/json": {"example": {"detail": "Pedido não encontrado"}}
            },
        },
    },
)
async def update(
    order: OrderUpdate,
    session: SessionDep,
    id: UUID = Path(description="Identificador do pedido"),
) -> ResponseUnit[OrderRead]:
    service = OrderService(session)
    data = await service.update_order(id, order)
    return ResponseUnit(data=data)


@router.delete(
    "/{id}/",
    status_code=204,
    dependencies=[Depends(is_administrator)],
    summary="Deleta um pedido específico",
    description="""
    ## 📝 Deleta um pedido específico
    Endpoint para excluir um pedido, removendo as linhas da tabela intermediária entre produto e pedido.
    
    ### 🔐 Permissões Necessárias
    - Apenas **administradores** podem excluir pedidos.

    ### 🔙 Retorno
    - Nenhum conteúdo é retornado, apenas o código HTTP 204 indicando um status de sucesso, mas sem conteúdo na resposta.
    """,
)
async def delete(
    session: SessionDep,
    id: UUID = Path(description="Identificador do pedido"),
):
    service = OrderService(session)
    data = await service.delete_order(id)
    return ResponseUnit(data=data)
