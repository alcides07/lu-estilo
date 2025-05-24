from typing import Optional
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(description="Nome da categoria", max_length=255)
    description: Optional[str] = Field(
        description="Descrição do produto", max_length=255
    )


class CategoryRead(CategoryBase):
    id: int = Field(description="Identificador da categoria")


class CategoryCreate(CategoryBase):
    pass
