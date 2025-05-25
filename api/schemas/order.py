from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID
from schemas.client import ClientRead
from pydantic import BaseModel, ConfigDict, Field


class OrderStatus(str, Enum):
    RECEIVED = "Recebido"
    WAITING_PAYMENT = "Aguardando pagamento"
    PAYMENT_APPROVED = "Pagamento aprovado"
    PREPARING = "Preparando"
    SHIPPED = "Enviado"
    OUT_FOR_DELIVERY = "Saiu para entrega"
    DELIVERED = "Entregue"
    CANCELLED = "Cancelado"
    RETURN_REQUESTED = "Devolução solicitada"
    REFUND_REQUESTED = "Reembolso solicitado"
    RETURNED = "Devolvido"
    REFUNDED = "Reembolsado"


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(description="Identificador do Pedido")
    date: datetime = Field(description="Data hora de realização do pedido")
    status: OrderStatus = Field(description="Status do pedido")
    client: Optional[ClientRead] = Field(
        description="Cliente que realizou o pedido", default=None
    )
    price_total: Decimal = Field(description="Valor total do pedido")


class ProductOrder(BaseModel):
    id: int = Field(description="Identificador do produto")
    quantity: int = Field(description="Quantidade desejada do produto", gt=0)


class OrderCreate(BaseModel):
    products: List[ProductOrder] = Field(
        description="Lista de produtos para incluir no pedido", min_length=1
    )


class OrderUpdate(BaseModel):
    status: OrderStatus = Field(description="Status do pedido")
