from sqlalchemy.orm import Session
from sqlalchemy import select


def exists(session: Session, model: type, **filters) -> bool:
    """Verifica se existe algum registro no modelo informado com os filtros especificados"""
    query = select(model)
    for field, value in filters.items():
        query = query.where(getattr(model, field) == value)
    return session.execute(query).scalar_one_or_none() is not None
