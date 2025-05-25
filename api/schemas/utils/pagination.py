from enum import Enum
from fastapi import Query
from pydantic import BaseModel, Field


class LimitPagination(int, Enum):
    CINCO = 5
    DEZ = 10
    QUINZE = 15
    VINTE = 20
    VINTE_CINCO = 25
    CINQUENTA = 50
    CEM = 100


class PaginationSchema:
    def __init__(
        self,
        limit: LimitPagination = Query(
            default=10, description="Quantidade de registros desejados"
        ),
        offset: int = Query(default=0, description="Intervalo inicial da paginação"),
    ):
        self.limit = limit
        self.offset = offset


class MetadataPagination(BaseModel):
    count: int = Field(
        description="Quantidade de registros da tabela em questão existentes no banco"
    )
