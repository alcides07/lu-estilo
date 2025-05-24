from dependencies.get_session_db import SessionDep
from models.user import User
from schemas.user import UserCreate
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from services.auth import get_password_hash


def create_user(user: UserCreate, session: SessionDep) -> User:
    user.password = get_password_hash(user.password)
    db_user = User(**user.model_dump(exclude=set(["passwordConfirmation"])))

    try:
        session.add(db_user)
        session.commit()
        return db_user

    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Database error"
        )  # ENVIAR PARA LOG
