from fastapi import Query


class CategoryFilter:
    def __init__(
        self,
        name: str = Query(
            default=None, max_length=255, description="Nome da categoria"
        ),
        description: str = Query(
            default=None, max_length=255, description="Descrição da categoria"
        ),
    ):
        self.name = name
        self.description = description
