from pydantic import BaseModel, ConfigDict, Field
from schemas.user import UserRead


class ClientRead(BaseModel):
    id: int = Field(description="Identificador do cliente")
    user: UserRead = Field(description="Usuário referente ao cliente")
    cpf: str = Field(max_length=11, description="CPF do cliente")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user": {
                    "created_at": "2025-05-26T11:47:47.573Z",
                    "email": "maria@email.com",
                    "id": 1,
                    "name": "maria",
                    "updated_at": "2025-05-26T11:47:47.573Z",
                },
                "cpf": "11122233344",
            }
        },
    )


class ClientCreate(BaseModel):
    user_id: int = Field(description="Identificador do usuário")
    cpf: str = Field(max_length=11, description="CPF do cliente")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"user_id": 1, "cpf": "11122233344"}},
    )


class ClientUpdate(BaseModel):
    cpf: str = Field(max_length=11, description="CPF do cliente")

    model_config = ConfigDict(
        from_attributes=True, json_schema_extra={"example": {"cpf": "11122233344"}}
    )
