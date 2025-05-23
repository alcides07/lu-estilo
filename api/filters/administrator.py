from fastapi import Query


class AdministratorFilter:
    def __init__(
        self,
        user__name: str = Query(
            default=None, max_length=255, description="Nome do usuário"
        ),
    ):
        self.user__name = user__name
