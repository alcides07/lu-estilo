from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserRead(BaseModel):
    name: str = Field(max_length=255, description="Nome do usuário")
    email: EmailStr = Field(max_length=255, description="E-mail do usuário")
    created_at: datetime = Field(description="Data de criação da conta do usuário")
    updated_at: datetime = Field(
        description="Data em que algum dado do usuário foi editado pela última vez"
    )


class UserCreate(BaseModel):
    name: str = Field(max_length=255, description="Nome do usuário")
    password: str = Field(max_length=32, description="Senha do usuário")
    email: EmailStr = Field(max_length=255, description="E-mail do usuário")
