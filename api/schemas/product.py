from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from schemas.category import CategoryRead


class ProductBase(BaseModel):
    description: str = Field(
        description="Descrição do produto",
        max_length=500,
    )
    value: Decimal = Field(
        description="Valor do produto",
        decimal_places=2,
        max_digits=12,
        ge=0,
    )
    bar_code: str = Field(description="Código de barras do produto")
    stock: int = Field(
        description="Estoque do produto",
        ge=0,
    )
    expiration_date: Optional[date] = Field(
        description="Data de validade do produto", default=None
    )


class ProductRead(ProductBase):
    id: int = Field(description="Identificador do produto")
    category: Optional[CategoryRead] = Field(
        description="Categoria a qual o produto pertence", default=None
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "description": "Jaqueta estilosa",
                "value": "78.90",
                "bar_code": "xxxx",
                "stock": 23,
                "expiration_date": "2026-05-26",
                "category": {
                    "id": 1,
                    "description": "Roupas de época",
                    "name": "Anos 80",
                },
            }
        }
    }


class ProductCreate(ProductBase):
    category_id: Optional[int] = Field(
        description="Identificador da categoria", default=None
    )

    @field_validator("expiration_date")
    def validate_expiration_date(cls, value):
        if value and value < date.today():
            raise ValueError("A data de validade não pode estar no passado")
        return value

    model_config = {
        "json_schema_extra": {
            "example": {
                "description": "Frango congelado",
                "value": 16.99,
                "bar_code": "xxxxxxxx",
                "stock": 32,
                "expiration_date": "2025-08-26",
                "category_id": 1,
            }
        }
    }


class ProductUpdate(ProductBase):
    category_id: Optional[int] = Field(
        description="Identificador da categoria", default=None
    )
