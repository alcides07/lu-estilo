from datetime import date
from fastapi import Query
from schemas.order import OrderStatus


class OrderFilter:
    def __init__(
        self,
        date__lte: date = Query(
            default=None, description="Data do pedido menor ou igual a"
        ),
        date__gte: date = Query(
            default=None, description="Data do pedido maior ou igual a"
        ),
        category_id: int = Query(
            default=None,
            description="Identificador da categoria para filtrar por pedidos que possuem produtos dessa categoria",
        ),
        status: OrderStatus = Query(default=None, description="Status do pedido"),
        client_id: int = Query(default=None, description="Identificador do cliente"),
    ):
        self.date__lte = date__lte
        self.date__gte = date__gte
        self.category_id = category_id
        self.status = status
        self.client_id = client_id
