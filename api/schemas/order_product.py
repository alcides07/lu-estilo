from decimal import Decimal
from typing import List
from schemas.order import OrderRead
from schemas.product import ProductRead
from pydantic import BaseModel, ConfigDict, Field


class ProductOfOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product: ProductRead = Field(description="Produto comprado no pedido")
    unit_price: Decimal = Field(
        description="Preço de cada unidade de produto comprada",
        max_digits=12,
        decimal_places=2,
    )
    quantity: int = Field(description="Quantidade de unidades compradas do produto")


class OrderProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order: OrderRead = Field(description="Dados do pedido")
    products: List[ProductOfOrder] = Field(description="Produtos do pedido")
