from typing import Type
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy import func


def count_collection(session, model: Type[BaseModel]):
    count_stmt = select(func.count()).select_from(model)
    return session.execute(count_stmt).scalar_one()
