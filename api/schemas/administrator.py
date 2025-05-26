from pydantic import BaseModel, Field
from schemas.user import UserRead


class AdministratorRead(BaseModel):
    id: int = Field(description="Identificador do Administrador")
    user: UserRead = Field(description="Usuário referente ao Administrator")

    class Config:
        schema_extra = {
            "example_list": {
                "metadata": {"count": 2},
                "data": [
                    {
                        "id": 1,
                        "user": {
                            "id": 1,
                            "name": "Admin Maria",
                            "email": "maria@email.com",
                            "created_at": "2025-05-26T06:17:51.214Z",
                            "updated_at": "2025-05-26T06:17:51.214Z",
                        },
                    },
                    {
                        "id": 2,
                        "user": {
                            "id": 2,
                            "name": "Admin Souza",
                            "email": "souza@email.com",
                            "created_at": "2024-01-22T06:17:51.214Z",
                            "updated_at": "2024-05-26T06:12:51.114Z",
                        },
                    },
                ],
            },
        }


class AdministratorCreate(BaseModel):
    user_id: int = Field(description="Identificador do usuário")

    class Config:
        schema_extra = {
            "exampĺe_in": {"user_id": 1},
            "example_out": {
                "id": 1,
                "user": {
                    "id": 1,
                    "name": "Admin João",
                    "email": "joao@email.com",
                    "created_at": "2022-05-26T06:58:35.965Z",
                    "updated_at": "2025-05-26T06:58:35.965Z",
                },
            },
        }
