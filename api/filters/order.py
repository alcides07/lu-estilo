from datetime import date
from fastapi import Query
from schemas.order import OrderStatus


class OrderFilter:
    def __init__(
        self,
        date__lte: date = Query(
            default=None,
            description="""
    Filtra por data do pedido menor ou igual a data informada.
    ### Características:
        - Exemplo: `?date__lte=2025-05-26` encontra todos os pedidos anteriores ou iguais ao dia 26 de maio de 2025.
    """,
        ),
        date__gte: date = Query(
            default=None,
            description="""
    Filtra por data do pedido maior ou igual a data informada.
    ### Características:
        - Exemplo: `?date__gte=2025-05-26` encontra todos os pedidos posteriores ou iguais ao dia 26 de maio de 2025.
    """,
        ),
        category_id: int = Query(
            default=None,
            description="""
    Filtra pedidos que possuem produtos da categoria informada.
    ### Características:
        - Exemplo: `?category_id=1` encontra todos os pedidos que possuem pelo menos 1 produto da categoria 1, mas que também podem existir produtos de outras categorias. 
    """,
        ),
        status: OrderStatus = Query(
            default=None,
            description="""
    Filtra por pedidos que possuem um status específico.
    ### Características:
        - Exemplo: `?status=Reembolsado` encontra todos os pedidos que foram reembolsados.
    """,
        ),
        client_id: int = Query(
            default=None,
            description="""
    Filtra por pedidos de um cliente específico.
    ### Características:
        - Exemplo: `?client_id=1` encontra todos os pedidos do cliente com identificador 1.
    """,
        ),
    ):
        self.date__lte = date__lte
        self.date__gte = date__gte
        self.category_id = category_id
        self.status = status
        self.client_id = client_id
