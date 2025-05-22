from api.dependencies.get_session_db import SessionDep
from api.models.user import User
from api.schemas.user import UserCreate


def create_user(user: UserCreate, session: SessionDep) -> User:
    db_user = User(**user.model_dump())

    with session.begin():
        session.add(db_user)
        session.flush()
        session.refresh(db_user)
        return db_user
