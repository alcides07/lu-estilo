from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(description="Nome da categoria", max_length=255)
    description: Optional[str] = Field(
        description="Descrição do produto", max_length=255
    )


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Identificador da categoria")


class CategoryCreate(CategoryBase):
    pass
