from decimal import Decimal
from fastapi import Query


class ProductFilter:
    def __init__(
        self,
        category_id: int = Query(
            default=None,
            description="""
    Filtra por categoria do produto através do identificador da categoria.
    ### Características:
        - Filtra por produtos de uma categoria específica.
        - Exemplo: `?category_id=1` encontra todos os produtos da categoria 1.
    """,
        ),
        value__lte: Decimal = Query(
            default=None,
            description="""
    Filtra por produtos que possuem o valor menor ou igual ao valor informado.
    - Exemplo: `?value__lte=100` encontra todos os produtos que possuem o valor igual ou menor a 100.
    """,
        ),
        value__gte: Decimal = Query(
            default=None,
            description="""
    Filtra por produtos que possuem o valor maior ou igual ao valor informado.
    - Exemplo: `?value__gte=100` encontra todos os produtos que possuem o valor igual ou maior a 100.
    """,
        ),
        stock__lte: str = Query(
            default=None,
            description="""
    Filtra por produtos que possuem o estoque menor ou igual ao estoque informado.
    - Exemplo: `?stock__lte=10` encontra todos os produtos que possuem o estoque igual ou menor que 100.
    """,
        ),
        stock__gte: str = Query(
            default=None,
            description="""
    Filtra por produtos que possuem o estoque maior ou igual ao estoque informado.
    - Exemplo: `?stock__gte=200` encontra todos os produtos que possuem o estoque igual ou maior que 200.
    """,
        ),
    ):
        self.category_id = category_id
        self.value__lte = value__lte
        self.value__gte = value__gte
        self.stock__lte = stock__lte
        self.stock__gte = stock__gte
