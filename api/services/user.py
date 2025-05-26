from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from services.auth import get_password_hash
from sqlalchemy.exc import SQLAlchemyError


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: UserCreate) -> User:
        user.password = get_password_hash(user.password)
        db_user = User(**user.model_dump(exclude=set(["passwordConfirmation"])))

        try:
            self.session.add(db_user)
            self.session.commit()
            return db_user

        except SQLAlchemyError:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
