from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Type, TypeVar, Any
from sqlalchemy.orm import DeclarativeBase

BaseModel = TypeVar("BaseModel", bound=DeclarativeBase)


def get_object_or_404(
    session: Session,
    model: Type[BaseModel],
    value: Any,
    column_name: str = "id",
    detail: str = "Object not found",
) -> BaseModel:
    column = getattr(model, column_name, None)

    if column is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Column '{column_name}' not found in model {model.__name__}",
        )

    obj = session.execute(select(model).where(column == value)).scalar_one_or_none()

    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    return obj
