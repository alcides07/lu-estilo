from fastapi import Query


class ClientFilter:
    def __init__(
        self,
        user__name: str = Query(
            default=None,
            max_length=255,
            description="""
    Filtra por nome do usuário.
    ### Características:
        - Busca por correspondência parcial (não distingue minúsculas e maiúsculas)
        - Máximo de 255 caracteres
        - Exemplo: `?user__name=ca` encontra "carol" e "carla"
    """,
        ),
        user__email: str = Query(
            default=None,
            max_length=255,
            description="""
    Filtra por e-mail do usuário.
    ### Características:
        - Busca por correspondência parcial (não distingue minúsculas e maiúsculas)
        - Máximo de 255 caracteres
        - Exemplo: `?user__email=car` encontra "carol@email.com" e "carla@email.com"
    """,
        ),
        cpf: str = Query(
            default=None,
            max_length=11,
            description="""
    Filtra por CPF do usuário.
    ### Características:
        - Busca por correspondência parcial
        - Máximo de 11 caracteres
        - Exemplo: `?cpf=555` encontra "555.444.333-22" e "333.444.555-66"
    """,
        ),
    ):
        self.cpf = cpf
        self.user__name = user__name
        self.user__email = user__email
