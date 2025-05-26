from fastapi import APIRouter, Body, Depends
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
    summary="Lista todos os administradores cadastrados",
    description="""
    ## 📝 Listagem de administradores
    Endpoint para consulta de todos os usuários administradores do sistema com filtragem e paginação de dados.
    
    ### 🔐 Permissões Necessárias
    - Exclusivo para usuários com perfil de administrador

    ### 🔎 Parâmetros de Filtro Disponíveis
    - **user__name** (string): Filtra administradores por correspondência parcial do nome
    """,
    responses={
        200: {
            "description": "Lista de administradores retornada com sucesso",
            "content": {
                "application/json": {
                    "example": AdministratorRead.Config.schema_extra["example_list"]
                }
            },
        },
        401: {
            "description": "Não autenticado",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            },
        },
        403: {
            "description": "Acesso negado por ser cliente",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
    },
)
async def list(
    session: SessionDep,
    pagination: PaginationSchema = Depends(),
    filters: AdministratorFilter = Depends(),
) -> ResponsePagination[AdministratorRead]:

    service = AdministratorService(session)
    data, metadata = service.list_administrators(pagination=pagination, filters=filters)
    return ResponsePagination(data=data, metadata=metadata)


@router.post(
    "/",
    response_model=AdministratorRead,
    status_code=201,
    summary="Cria um novo administrador (associando a um usuário existente)",
    description="""
    ## 📝 Cadastro de administradores
    Endpoint para cadastrar um novo administrador no sistema, vinculando-o a um usuário criado anteriormente (via POST /auth/register/).
    Basta informar o identificador do usuário (user_id) no momento da submissão.
         
    ### 🔐 Permissões Necessárias
    - Qualquer usuário **logado** pode se colocar como administrador, mas não pode colocar outros usuários.
    
    ### 🚨 Importante
    - Ao se colocar como administrador, deve-se deslogar e realizar um novo login via (POST /auth/login/) para que as permissões de administrador entrem em vigor.
    """,
    responses={
        201: {
            "description": "Objeto de administrador atribuído com sucesso",
            "content": {
                "application/json": {
                    "example": AdministratorCreate.Config.schema_extra["example_out"]
                }
            },
        },
        401: {
            "description": "Não autenticado",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            },
        },
        403: {
            "description": "Acesso negado ao tentar vincular administrador a outro usuário",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
    },
)
async def create(
    session: SessionDep,
    current_user: User = Depends(get_user_authenticated),
    administrator: AdministratorCreate = Body(
        openapi_examples={
            "exemplo_1": {
                "summary": "Envio de {user_id}",
                "value": AdministratorCreate.Config.schema_extra["exampĺe_in"],
            },
        },
    ),
):
    await check_ower_user_permission(administrator.user_id, current_user)

    service = AdministratorService(session)
    return service.create_administrator(administrator)
