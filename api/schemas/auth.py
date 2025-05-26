from datetime import timedelta
from typing import List
from pydantic import BaseModel, Field
from enum import Enum
from schemas.role import Role


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class LoginOut(BaseModel):
    access_token: str = Field(description="Token de acesso")
    refresh_token: str = Field(description="Token de atualização")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJzdWIiOiJhZG1pbiIsInJvbGVzIjpbImNsaWVudCIsImFkbWluaXN0cmF0b3IiXSwiZXhwIjoxNzQ4MjY0Njc5LCJ0b2tlbl90eXBlIjoiYWNjZXNzIn0.qMKY14EAUkQLHTpe_NEePLMppGmjTyLWf4m4uSPqUZw",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJzdWIiOiJhZG1pbiIsInJvbGVzIjpbImNsaWVudCIsImFkbWluaXN0cmF0b3IiXSwiZXhwIjoxNzQ4MzUwNzc5LCJ0b2tlbl90eXBlIjoicmVmcmVzaCJ9.M4_bSlr2kHex0g3HRCHVElMcIjP-DfzEhTEmwmjlbCo",
            },
        }
    }


class TokenRefreshIn(BaseModel):
    """Dados que são submetidos para obter um novo token de acesso"""

    refresh: str = Field(description="Token de atualização")


class TokenRefreshOut(BaseModel):
    """Dados que são retornados após solicitação de refresh token"""

    access: str = Field(description="Novo token de acesso")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJzdWIiOiJhZG1pbiIsInJvbGVzIjpbImNsaWVudCIsImFkbWluaXN0cmF0b3IiXSwiZXhwIjoxNzQ4MjY0Njc5LCJ0b2tlbl90eXBlIjoiYWNjZXNzIn0.qMKY14EAUkQLHTpe_NEePLMppGmjTyLWf4m4uSPqUZw",
            },
        }
    }


class TokenStorage(BaseModel):
    """Dados que estão armazenados dentro do token JWT"""

    user_id: int = Field(description="Identificador do usuário")
    sub: str = Field(description="Nome do usuário")
    token_type: TokenType = Field(description="Tipo do token")
    exp: timedelta = Field(description="Tempo de expiração do token")
    roles: List[Role]


class TokenDataToSubmitToStorage(BaseModel):
    """Dados utilizados como entrada para a geração de tokens JWT."""

    user_id: int = Field(description="Identificador do usuário")
    sub: str = Field(description="Nome do usuário")
    roles: List[Role] = Field(description="Lista de papéis que o usuário possui")
