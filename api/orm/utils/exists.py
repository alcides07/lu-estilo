from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql import exists as sql_exists


def exists(session: Session, model: type, **filters) -> bool:
    stmt = sql_exists().where(
        *(getattr(model, field) == value for field, value in filters.items())
    )
    result = session.execute(select(stmt)).scalar()
    return result if result is not None else False
