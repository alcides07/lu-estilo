from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime


class UserRead(BaseModel):
    id: int = Field(description="Identificador do usuário")
    name: str = Field(max_length=255, description="Nome do usuário")
    email: EmailStr = Field(max_length=255, description="E-mail do usuário")
    created_at: datetime = Field(description="Data de criação da conta do usuário")
    updated_at: datetime = Field(
        description="Data em que algum dado do usuário foi editado pela última vez"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "maria",
                "email": "maria@email.com",
                "created_at": "2025-05-26T11:47:47.573Z",
                "updated_at": "2025-05-26T11:47:47.573Z",
            }
        },
    )


class UserCreate(BaseModel):
    name: str = Field(max_length=255, description="Nome do usuário")
    password: str = Field(max_length=255, description="Senha do usuário")
    email: EmailStr = Field(max_length=255, description="E-mail do usuário")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "maria",
                "password": "123456",
                "email": "maria@email.com",
            }
        },
    )
