from pydantic import BaseModel, Field
from schemas.user import UserRead


class AdministratorRead(BaseModel):
    id: int = Field(description="Identificador do Administrador")
    user: UserRead = Field(description="Usuário referente ao Administrator")


class AdministratorCreate(BaseModel):
    user_id: int = Field(description="Identificador do usuário")
