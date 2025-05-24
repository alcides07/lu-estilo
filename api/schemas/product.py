from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from api.schemas.category import CategoryRead


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
    expiration_date: date = Field(description="Data de validade do produto")


class ProductRead(ProductBase):
    id: int = Field(description="Identificador do produto")
    category: Optional[CategoryRead] = Field(
        description="Categoria a qual o produto pertence", default=None
    )


class ProductCreate(ProductBase):
    category_id: Optional[int] = Field(
        description="Identificador da categoria", default=None
    )

    @field_validator("expiration_date")
    def validate_expiration_date(cls, value):
        if value and value < date.today():
            raise ValueError("A data de validade não pode estar no passado")
        return value


class ProductUpdate(ProductBase):
    category_id: Optional[int] = Field(
        description="Identificador da categoria", default=None
    )
