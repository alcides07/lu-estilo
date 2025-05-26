from decimal import Decimal
from typing import List
from schemas.order import OrderRead
from schemas.product import ProductRead
from pydantic import BaseModel, ConfigDict, Field


class ProductOfOrder(BaseModel):
    product: ProductRead = Field(description="Produto comprado no pedido")
    unit_price: Decimal = Field(
        description="Preço de cada unidade de produto comprada",
        max_digits=12,
        decimal_places=2,
    )
    quantity: int = Field(description="Quantidade de unidades compradas do produto")

    model_config = ConfigDict(from_attributes=True)


class OrderProductRead(BaseModel):

    order: OrderRead = Field(description="Dados do pedido")
    products: List[ProductOfOrder] = Field(description="Produtos do pedido")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "order": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "date": "2025-05-26T17:51:08.197Z",
                    "status": "Entregue",
                    "client": {
                        "cpf": "11122233344",
                        "id": 1,
                        "user": {
                            "created_at": "2025-05-26T11:47:47.573Z",
                            "email": "maria@email.com",
                            "id": 1,
                            "name": "maria",
                            "updated_at": "2025-05-26T11:47:47.573Z",
                        },
                    },
                    "price_total": "150.00",
                },
                "products": [
                    {
                        "product": {
                            "bar_code": "xxxx",
                            "category": {
                                "description": "Roupas de época",
                                "id": 1,
                                "name": "Anos 80",
                            },
                            "description": "Jaqueta estilosa",
                            "expiration_date": "2026-05-26",
                            "id": 1,
                            "stock": 23,
                            "value": "75.00",
                        },
                        "unit_price": "75.00",
                        "quantity": 2,
                    }
                ],
            }
        },
    )
