from datetime import timedelta
from pydantic import BaseModel, Field
from enum import Enum


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class LoginOut(BaseModel):
    access_token: str = Field(description="Token de acesso")
    refresh_token: str = Field(description="Token de atualização")


class TokenRefreshIn(BaseModel):
    """Dados que são submetidos para obter um novo token de acesso"""

    refresh: str = Field(description="Token de atualização")


class TokenRefreshOut(BaseModel):
    """Dados que são retornados após solicitação de refresh token"""

    access: str = Field(description="Novo token de acesso")


class TokenStorage(BaseModel):
    """Dados que são armazenados dentro do token JWT"""

    user_id: int = Field(description="Identificador do usuário")
    sub: str = Field(description="Nome do usuário")
    token_type: TokenType = Field(description="Tipo do token")
    exp: timedelta = Field(description="Tempo de expiração do token")
