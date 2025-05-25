from pydantic import BaseModel, ConfigDict, Field
from schemas.user import UserRead


class ClientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Identificador do cliente")
    user: UserRead = Field(description="Usuário referente ao cliente")
    cpf: str = Field(max_length=11, description="CPF do cliente")


class ClientCreate(BaseModel):
    user_id: int = Field(description="Identificador do usuário")
    cpf: str = Field(max_length=11, description="CPF do cliente")


class ClientUpdate(BaseModel):
    cpf: str = Field(max_length=11, description="CPF do cliente")
