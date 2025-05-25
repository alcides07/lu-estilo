from typing import Optional, Type, TypeVar
from fastapi import HTTPException, status
from orm.utils.count_collection import count_collection
from dependencies.get_session_db import SessionDep
from schemas.utils.pagination import MetadataPagination, PaginationSchema
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
    total_count = count_collection(session, model)

    stmt = apply_filters(stmt, model, filters)
    stmt = apply_pagination(stmt, pagination)

    data = session.execute(stmt).scalars().all()
    metadata = MetadataPagination(count=total_count)

    return data, metadata


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
                status.HTTP_400_BAD_REQUEST,
                f"Relacionamento '{part}' não encontrado em {current_model.__name__}",
            )

        stmt = stmt.join(getattr(current_model, part))
        current_model = getattr(current_model, part).property.mapper.class_

    final_field = parts[-1]
    if not hasattr(current_model, final_field):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Campo '{final_field}' não encontrado em {current_model.__name__}",
        )

    column = getattr(current_model, final_field)
    if not isinstance(column.type, String):
        column = cast(column, String)

    return stmt.where(column.ilike(f"%{value}%"))


def apply_comparison_filters(stmt, model: Type[BaseModel], attr: str, value):
    """Aplica filtros de comparação (lte, gte, lt, gt, eq, ne)"""
    parts = attr.split("__")
    field_name = parts[0]
    operator = parts[1]

    if not hasattr(model, field_name):
        return stmt

    column = getattr(model, field_name)

    operators = {
        "lte": column <= value,
        "gte": column >= value,
        "lt": column < value,
        "gt": column > value,
        "eq": column == value,
        "ne": column != value,
    }

    if operator in operators:
        return stmt.where(operators[operator])

    return stmt


def apply_filters(stmt, model: Type[BaseModel], filters: Optional[T] = None):
    """Apply filter conditions to the query"""
    if not filters:
        return stmt

    COMPARISON_OPERATORS = {"lte", "gte", "lt", "gt", "eq", "ne"}

    for attr, value in filters.__dict__.items():
        if value is None:
            continue

        if "__" in attr:  # Filtro aninhado
            parts = attr.split("__")
            operator = parts[1] if len(parts) > 1 else None
            if operator in COMPARISON_OPERATORS:  # Operadores de comparação
                stmt = apply_comparison_filters(stmt, model, attr, value)
            else:  # Submodelos
                stmt = apply_nested_filter(stmt, model, attr, value)

        else:  # Filtro comum (atributo simples)
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
