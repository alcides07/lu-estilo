from fastapi import Query


class CategoryFilter:
    def __init__(
        self,
        name: str = Query(
            default=None,
            max_length=255,
            description="""
    Filtra por nome (ou parte do nome) da categoria.
    ### Características:
        - Busca por correspondência parcial (não distingue minúsculas e maiúsculas)
        - Máximo de 255 caracteres
        - Exemplo: `?name=ca` encontra "camisas" e "casacos"
    """,
        ),
        description: str = Query(
            default=None,
            max_length=255,
            description="""
    Filtra por descrição (ou parte da descrição) da categoria.
    ### Características:
        - Busca por correspondência parcial (não distingue minúsculas e maiúsculas)
        - Máximo de 255 caracteres
        - Exemplo: `?description=promoção` encontra "promoção de casacos" e "promoção de shorts"
    """,
        ),
    ):
        self.name = name
        self.description = description
