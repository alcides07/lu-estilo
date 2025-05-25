from pydantic import BaseModel, Field
from typing import TypeVar, List, Generic
from schemas.utils.pagination import MetadataPagination

T = TypeVar("T")


class ResponsePagination(BaseModel, Generic[T]):
    metadata: MetadataPagination = Field(description="Metadados da paginação")
    data: List[T] = Field(description="Lista de objetos retornados")


class ResponseUnit(BaseModel, Generic[T]):
    data: T = Field(description="Objeto retornado")
