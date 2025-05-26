from typing import Annotated
from fastapi import APIRouter, Depends
from services.user import UserService
from dependencies.get_session_db import SessionDep
from schemas.auth import (
    LoginOut,
    TokenDataToSubmitToStorage,
    TokenRefreshIn,
    TokenRefreshOut,
    TokenType,
)
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate, UserRead
from schemas.utils.get_roles_from_user import get_roles_from_user
from services.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/register/",
    status_code=201,
    summary="Cadastra um novo usuário no sistema",
    description="""
    ## 📝 Registro de usuários
    Endpoint para registrar usuários no sistema.
    
    ### 🔐 Permissões
    - Não há restrição de permissão para o cadastro de usuário, portanto qualquer pessoa não autenticada pode realizar.
    
    ### 📑 Regras de negócio
    - Os campos de "name" e "email" devem ser únicos. Um erro será disparado se existir alguma conta com alguma dessas informações.
    
    ### ⬇️ Campos do formulário
    - 'name'     (OBRIGATÓRIO): Nome do usuário com no máximo de 255 caracteres
    - 'password' (OBRIGATÓRIO): Senha do usuário com no máximo de 255 caracteres
    - 'email'    (OBRIGATÓRIO): E-mail válido para o usuário com no máximo 255 caracteres
    
    ### 💬 Observações:
    - Após o cadastro da conta de usuário, é possível vinculá-lo tanto a um cliente (via POST /clients/) quanto a um administrador (via POST /administrators/), fazendo com que ele tenha permissão dos dois papéis.
    """,
    responses={
        400: {
            "description": "Erros gerados por ação do usuário",
            "content": {
                "application/json": {
                    "examples": {
                        "nome_existente": {
                            "summary": "Nome já em uso",
                            "value": {"detail": "Já existe um usuário com esse nome"},
                        },
                        "email_existente": {
                            "summary": "E-mail já em uso",
                            "value": {"detail": "Já existe um usuário com esse e-mail"},
                        },
                    }
                }
            },
        },
    },
)
async def create(session: SessionDep, user: UserCreate) -> UserRead:
    service = UserService(session)
    return service.create_user(user)


@router.post(
    "/login/",
    summary="Realiza a autenticação de um usuário no sistema",
    description="""
    ## 📝 Login de usuários
    Endpoint para realizar o login no sistema.
    
    ### 🔐 Permissões
    - Qualquer usuário cadastrado pode realizar login no sistema informando suas credenciais corretamente.
    
    ### 📑 Regras de negócio
    - Caso você tenha sido vinculado a um perfil de cliente ou administrador na sessão atual, é necessário realizar um novo login para que as permissões de "cliente" e/ou "administrador" entrem em vigor.    
    
    ### ⬇️ Campos do formulário
    - grant_type     (OBRIGATÓRIO): Deve ter um valor igual a 'password' 
    - username       (OBRIGATÓRIO): Nome do usuário
    - password       (OBRIGATÓRIO): Senha do usuário
    - *scope         (OPCIONAL): Escopos de permissão do usuário
    - *client_id     (OPCIONAL): Identificador único para o cliente
    - *client_secret (OPCIONAL): Chave secreta para o cliente
    
    * Campos que não surtirão efeitos caso submetidos no momento do login    
    
    ### 🔙 Retorno
    - São retornados dois tokens:
       - 'access_token':  Token utilizado nas requisições para ter acesso a aplicação, com expiração de **5 minutos**.
       - 'refresh_token': Token de atualização com expiração de **1 dia**, a ser utilizado para obter novos tokens de acesso durante esse período.
    """,
    responses={
        401: {
            "description": "Credenciais inválidas ou inexistentes",
            "content": {
                "application/json": {"example": {"detail": "Credenciais inválidas"}},
            },
        },
    },
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> LoginOut:
    user = authenticate_user(session, form_data.username, form_data.password)
    data_token = TokenDataToSubmitToStorage(
        sub=user.name,
        user_id=user.id,
        roles=get_roles_from_user(user),
    )

    access_token = await create_access_token(data_token)
    refresh_token = await create_refresh_token(data_token)

    return LoginOut(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/refresh-token/",
    summary="Gera um novo token de acesso",
    description="""
    ## 📝 Solicitação de novo token de acesso
    Endpoint para solicitar um novo token de acesso para continuar utilizando a aplicação.
    
    ### 🔐 Permissões
    - Qualquer usuário pode solicitar um novo token de acesso.
    
    ### 📑 Regras de negócio
    - Um novo token de acesso só é gerado quando o token de atualização fornecido estiver válido (dentro do prazo de expiração) e íntegro.    
    
    ### ⬇️ Campos do formulário
    - refresh (OBRIGATÓRIO): Token de atualização válido
    
    ### 🔙 Retorno
    - É retornado um novo token de acesso, denominado 'access_token':
    """,
    responses={
        401: {
            "description": "Erros no token",
            "content": {
                "application/json": {
                    "examples": {
                        "token_expirado": {
                            "summary": "O token de atualização expirou",
                            "value": {"detail": "Token expirado"},
                        },
                        "token_invalido": {
                            "summary": "O token de atualização está inválido",
                            "value": {"detail": "Token inválido"},
                        },
                    }
                }
            },
        },
    },
)
async def refresh_access_token(
    refresh: TokenRefreshIn,
) -> TokenRefreshOut:
    user_data = await verify_token(refresh.refresh, TokenType.REFRESH)

    new_access_token = await create_access_token(
        data={"sub": user_data.sub, "user_id": user_data.user_id}
    )
    return TokenRefreshOut(access=new_access_token)
