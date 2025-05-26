from fastapi import Query


class AdministratorFilter:
    def __init__(
        self,
        user__name: str = Query(
            default=None,
            max_length=255,
            description="""
    Filtra por nome (ou parte do nome) do administrador.
    ### Características:
        - Busca por correspondência parcial (não distingue minúsculas e maiúsculas)
        - Máximo de 255 caracteres
        - Exemplo: `?user__name=mar` encontra "Maria" e "Mario"
    """,
        ),
    ):
        self.user__name = user__name
