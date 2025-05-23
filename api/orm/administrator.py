from api.dependencies.get_session_db import SessionDep
from api.models.administrator import Administrator
from api.models.user import User
from api.schemas.administrator import AdministratorCreate
from api.orm.utils.get_object_or_404 import get_object_or_404
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from api.services.administrator import check_user_administrator_exists


def create_administrator(
    administrator: AdministratorCreate, session: SessionDep
) -> Administrator:
    db_administrator = Administrator(**administrator.model_dump())
    get_object_or_404(
        session, User, administrator.user_id, detail="Usuário não encontrado"
    )
    check_user_administrator_exists(session, administrator.user_id)

    try:
        session.add(db_administrator)
        session.commit()
        return db_administrator

    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Database error")  # ENVIAR PARA LOG
