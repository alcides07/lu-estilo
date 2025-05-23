from api.dependencies.get_session_db import SessionDep
from api.models.user import User
from api.schemas.user import UserCreate
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from api.services.auth import get_password_hash
from api.services.user import check_email_exists, check_name_exists


def create_user(user: UserCreate, session: SessionDep) -> User:
    check_email_exists(session, user.email)
    check_name_exists(session, user.name)

    user.password = get_password_hash(user.password)
    db_user = User(**user.model_dump(exclude=set(["passwordConfirmation"])))

    try:
        session.add(db_user)
        session.commit()
        return db_user

    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Database error")  # ENVIAR PARA LOG
