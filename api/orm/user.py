from api.dependencies.get_session_db import SessionDep
from api.models.user import User
from api.schemas.user import UserCreate
from passlib.context import CryptContext
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from api.services.user import check_email_exists

pwd_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(user: UserCreate, session: SessionDep) -> User:
    check_email_exists(session, user.email)

    user.password = get_password_hash(user.password)
    db_user = User(**user.model_dump(exclude=set(["passwordConfirmation"])))

    try:
        session.add(db_user)
        session.commit()
        return db_user

    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Database error")  # ENVIAR PARA LOG
