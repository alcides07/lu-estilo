from pydantic import BaseModel, ConfigDict, Field
from schemas.user import UserRead


class AdministratorRead(BaseModel):
    id: int = Field(description="Identificador do Administrador")
    user: UserRead = Field(description="Usuário referente ao Administrator")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "user": {
                        "id": 1,
                        "name": "Admin Maria",
                        "email": "maria@email.com",
                        "created_at": "2025-05-26T06:17:51.214Z",
                        "updated_at": "2025-05-26T06:17:51.214Z",
                    },
                }
            ],
        },
    )


class AdministratorCreate(BaseModel):
    user_id: int = Field(description="Identificador do usuário")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {"user_id": 1},
        },
    )
