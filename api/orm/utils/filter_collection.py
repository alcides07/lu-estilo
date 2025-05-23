from typing import Optional, Type, TypeVar
from fastapi import HTTPException
from api.dependencies.get_session_db import SessionDep
from api.schemas.utils.pagination import PaginationSchema
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, String
from sqlalchemy.sql.expression import cast

BaseModel = TypeVar("BaseModel", bound=DeclarativeBase)
T = TypeVar("T")


def filter_collection(
    session: SessionDep,
    model: Type[BaseModel],
    pagination: PaginationSchema,
    filters: Optional[T] = None,
):
    """Main function to filter and paginate a collection"""
    stmt = select(model)

    stmt = apply_filters(stmt, model, filters)
    stmt = apply_pagination(stmt, pagination)

    data = session.execute(stmt).scalars().all()

    return data


def apply_nested_filter(stmt, model: Type[BaseModel], field_path: str, value: str):
    """
    Aplica filtro em relacionamento aninhado usando sintaxe com '__'
    Exemplo: 'user__name' -> model.user.name
    """
    parts = field_path.split("__")
    current_model = model

    for part in parts[:-1]:
        if not hasattr(current_model, part):
            raise HTTPException(
                400,
                f"Relacionamento '{part}' não encontrado em {current_model.__name__}",
            )

        stmt = stmt.join(getattr(current_model, part))
        current_model = getattr(current_model, part).property.mapper.class_

    final_field = parts[-1]
    if not hasattr(current_model, final_field):
        raise HTTPException(
            400, f"Campo '{final_field}' não encontrado em {current_model.__name__}"
        )

    column = getattr(current_model, final_field)
    if not isinstance(column.type, String):
        column = cast(column, String)

    return stmt.where(column.ilike(f"%{value}%"))


def apply_filters(stmt, model: Type[BaseModel], filters: Optional[T] = None):
    """Apply filter conditions to the query"""
    if not filters:
        return stmt

    for attr, value in filters.__dict__.items():
        if value is None:
            continue

        if "__" in attr:  # Filtro aninhado
            stmt = apply_nested_filter(stmt, model, attr, value)

        else:  # Filtro comum
            if hasattr(model, attr):
                column = getattr(model, attr)
                if not isinstance(column.type, String):
                    column = cast(column, String)
                stmt = stmt.where(column.ilike(f"%{value}%"))

    return stmt


def apply_pagination(stmt, pagination: PaginationSchema):
    """Apply pagination to the query"""
    if pagination:
        stmt = stmt.offset(pagination.offset).limit(pagination.limit)
    return stmt
