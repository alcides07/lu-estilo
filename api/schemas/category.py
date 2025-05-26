from typing import Optional
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(description="Nome da categoria", max_length=255)
    description: Optional[str] = Field(
        description="Descrição do produto", max_length=255
    )


class CategoryRead(CategoryBase):
    id: int = Field(description="Identificador da categoria")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "inverno",
                "description": "roupas de inverno",
            }
        }
    }


class CategoryCreate(CategoryBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "inverno",
                "description": "roupas de inverno",
            }
        }
    }
