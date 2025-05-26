from fastapi import APIRouter, Depends, Path, Response, status
from permissions.user import check_ower_user_permission
from permissions.client import check_owner_client_permission
from services.client import ClientService
from dependencies.get_user_authenticated import get_user_authenticated
from dependencies.get_session_db import SessionDep
from filters.client import ClientFilter
from models.client import Client
from models.user import User
from permissions.administrator import is_administrator
from schemas.client import ClientCreate, ClientRead, ClientUpdate
from schemas.utils.pagination import PaginationSchema
from schemas.utils.responses import ResponsePagination, ResponseUnit


router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    dependencies=[Depends(get_user_authenticated)],
)


@router.get(
    "/",
    dependencies=[Depends(is_administrator)],
    summary="Lista todos os clientes cadastrados",
    description="""
    ## 📝 Listagem de clientes
    Endpoint para consulta de todos os clientes do sistema com filtragem e paginação dos dados.
    
    ### 🔐 Permissões Necessárias
    - É necessário ser **administrador**.

    ### 🔎 Parâmetros de Filtro Disponíveis
    - limit       (int): Indica a quantidade de clientes que deseja visualizar
    - offset      (int): Indica a partir de qual cliente da lista deseja visualizar
    - user__name  (str): Filtra clientes por correspondência parcial do nome de usuário
    - user__email (str): Filtra clientes por correspondência parcial do e-mail
    - cpf         (str): Filtra clientes por correspondência parcial do CPF
    """,
    responses={
        403: {
            "description": "Acesso negado por ser cliente",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
    },
)
async def list(
    session: SessionDep,
    pagination: PaginationSchema = Depends(),
    filters: ClientFilter = Depends(),
) -> ResponsePagination[ClientRead]:

    service = ClientService(session)
    data, metadata = service.list_clients(pagination=pagination, filters=filters)
    return ResponsePagination(data=data, metadata=metadata)


@router.get(
    "/{id}/",
    summary="Visualiza os dados de um cliente específico",
    description="""
    ## 📝 Visualiza os dados de um cliente
    Endpoint para visualizar os dados de um cliente.
    
    ### 🔐 Permissões Necessárias
    - Apenas o próprio cliente tem permissão para visualizar os dados de sua conta.
    
    ### 🔙 Retorno
    - São retornados os dados do usuário vinculado (id, name, email, created_at e updated_at), além do CPF do cliente.
    """,
    responses={
        403: {
            "description": "Tentativa de visualizar os dados de outro cliente",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": "Cliente não encontrado com identificador informado",
            "content": {
                "application/json": {"example": {"detail": "Cliente não encontrado"}}
            },
        },
    },
)
async def read(
    session: SessionDep,
    id: int = Path(description="Identificador do cliente"),
    _: Client = Depends(check_owner_client_permission),
) -> ResponseUnit[ClientRead]:

    service = ClientService(session)
    data = await service.read_client(id)
    return ResponseUnit(data=data)


@router.post(
    "/",
    status_code=201,
    summary="Cadastra um novo cliente",
    description="""
    ## 📝 Cadastra um novo cliente
    Endpoint para cadastrar um novo cliente no sistema, vinculando-o a um usuário criado anteriormente (via POST /auth/register/).
    Basta informar o identificador do usuário (user_id) no momento da submissão.
    
    ### 🔐 Permissões Necessárias
    - Só é permitido cadastrar um cliente para seu próprio usuário logado (que está solicitando o cadastro), não sendo possível cadastrar clientes para vínculo com outros usuários existentes.

    ### 🚨 Importante
    - Ao se colocar como cliente, deve-se deslogar e realizar um novo login via (POST /auth/login/) para que as permissões de cliente entrem em vigor.

    ### ⬇️ Campos do formulário
    - user_id (OBRIGATÓRIO): Identificador do usuário para vincular com conta cliente
    - cpf     (OBRIGATÓRIO): CPF do cliente
    
    ### 🔙 Retorno
    - São retornados os dados do usuário vinculado (id, name, email, created_at e updated_at), além dos dados do cliente (CPF).
    """,
    responses={
        400: {
            "description": "Cliente já existente com usuário",
            "content": {
                "application/json": {
                    "examples": {
                        "cpf_invalido": {
                            "summary": "O CPF submetido não é válido",
                            "value": {"detail": "CPF inválido"},
                        },
                        "usuario_existente": {
                            "summary": "Cliente já existente com usuário",
                            "value": {
                                "detail": "Já existe um cliente associado a esse usuário"
                            },
                        },
                        "cpf_existente": {
                            "summary": "Cliente já existente com CPF",
                            "value": {"detail": "Já existe um cliente com esse CPF"},
                        },
                    }
                },
            },
        },
        403: {
            "description": "Tentativa de cadastrar um cliente para outro usuário",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": "Cliente não encontrado com identificador informado",
            "content": {
                "application/json": {"example": {"detail": "Cliente não encontrado"}}
            },
        },
    },
)
async def create(
    client: ClientCreate,
    session: SessionDep,
    current_user: User = Depends(get_user_authenticated),
) -> ClientRead:
    await check_ower_user_permission(client.user_id, current_user)
    service = ClientService(session)
    return service.create_client(client)


@router.put(
    "/{id}/",
    summary="Edita dados de um cliente específico",
    description="""
    ## 📝 Edita os dados de um cliente
    Endpoint para editar os dados de um cliente, atualizando-os na base de dados.
    
    ### 🔐 Permissões Necessárias
    - Apenas o próprio cliente tem permissão para editar os dados de sua conta.
    
    ### ⬇️ Campos do formulário
    - cpf (OBRIGATÓRIO): CPF do cliente
    
    ### 🔙 Retorno
    - São retornados os dados do usuário vinculado (id, name, email, created_at e updated_at), além do CPF atualizado do cliente.
    """,
    responses={
        400: {
            "description": "Erro após submissão errada do usuário",
            "content": {
                "application/json": {
                    "examples": {
                        "cpf_invalido": {
                            "summary": "O CPF submetido não é válido",
                            "value": {"detail": "CPF inválido"},
                        },
                        "cpf_existente": {
                            "summary": "Cliente já existente com CPF",
                            "value": {"detail": "Já existe um cliente com esse CPF"},
                        },
                    }
                },
            },
        },
        403: {
            "description": "Tentativa de editar os dados de outro cliente",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": "Cliente não encontrado com o identificador informado",
            "content": {
                "application/json": {"example": {"detail": "Cliente não encontrado"}}
            },
        },
    },
)
async def update(
    client: ClientUpdate,
    session: SessionDep,
    id: int = Path(description="Identificador do cliente"),
    _: Client = Depends(check_owner_client_permission),
) -> ClientRead:
    service = ClientService(session)
    data = service.update_client(client, id)
    return data


@router.delete(
    "/{id}/",
    status_code=204,
    summary="Exclui um cliente específico",
    description="""
    ## 📝 Exclui o cliente e sua conta de usuário
    Endpoint para excluir a conta de um cliente, removendo os dados da base.
    
    ### 🔐 Permissões Necessárias
    - Apenas o próprio cliente tem permissão para deletar sua conta.

    ### 🔙 Retorno
    - Nenhum conteúdo é retornado, apenas o código HTTP 204 indicando um status de sucesso, mas sem conteúdo na resposta.
    """,
)
async def delete(
    session: SessionDep,
    id: int = Path(description="Identificador do cliente"),
    _: Client = Depends(check_owner_client_permission),
):
    service = ClientService(session)
    await service.delete_client(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
