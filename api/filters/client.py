from fastapi import Query


class ClientFilter:
    def __init__(
        self,
        user__name: str = Query(
            default=None, max_length=255, description="Nome do usuário"
        ),
        user__email: str = Query(
            default=None, max_length=255, description="E-mail do usuário"
        ),
        cpf: str = Query(default=None, max_length=11, description="CPF do cliente"),
    ):
        self.cpf = cpf
        self.user__name = user__name
        self.user__email = user__email
