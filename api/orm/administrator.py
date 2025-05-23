from api.dependencies.get_session_db import SessionDep
from api.filters.administrator import AdministratorFilter
from api.models.administrator import Administrator
from api.models.user import User
from api.orm.utils.filter_collection import filter_collection
from api.schemas.administrator import AdministratorCreate
from api.orm.utils.get_object_or_404 import get_object_or_404
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.utils.pagination import PaginationSchema


def list_administrators(
    session: SessionDep, pagination: PaginationSchema, filters: AdministratorFilter
):
    data = filter_collection(
        session,
        model=Administrator,
        pagination=pagination,
        filters=filters,
    )
    return data


def create_administrator(
    administrator: AdministratorCreate, session: SessionDep
) -> Administrator:
    get_object_or_404(
        session, User, administrator.user_id, detail="Usuário não encontrado"
    )
    db_administrator = Administrator(**administrator.model_dump())

    try:
        session.add(db_administrator)
        session.commit()
        return db_administrator

    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Database error"
        )  # ENVIAR PARA LOG
