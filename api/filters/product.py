from decimal import Decimal
from fastapi import Query


class ProductFilter:
    def __init__(
        self,
        category_id: int = Query(
            description="Identificador da categoria", default=None
        ),
        value__lte: Decimal = Query(
            description="Menor ou igual - Valor do produto", default=None
        ),
        value__gte: Decimal = Query(
            description="Maior ou igual - Valor do produto", default=None
        ),
        stock__lte: str = Query(
            description="Menor ou igual - Estoque do produto", default=None
        ),
        stock__gte: str = Query(
            description="Maior ou igual - Estoque do produto", default=None
        ),
    ):
        self.category_id = category_id
        self.value__lte = value__lte
        self.value__gte = value__gte
        self.stock__lte = stock__lte
        self.stock__gte = stock__gte
