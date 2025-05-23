from fastapi import Query


class ClientFilter:
    def __init__(
        self,
        user__name: str = Query(
            default=None, max_length=255, description="Nome do usuário"
        ),
        cpf: str = Query(default=None, max_length=11, description="CPF do cliente"),
    ):
        self.cpf = cpf
        self.user__name = user__name
