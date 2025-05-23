from pydantic import BaseModel, Field
from typing import TypeVar, List, Generic

T = TypeVar("T")


class ResponsePagination(BaseModel, Generic[T]):
    data: List[T] = Field(description="Lista de objetos retornados")
