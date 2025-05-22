from api.dependencies.get_session_db import SessionDep
from api.models.user import User
from api.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(user: UserCreate, session: SessionDep) -> User:
    user.password = get_password_hash(user.password)
    db_user = User(**user.model_dump(exclude=set(["passwordConfirmation"])))

    with session.begin():
        session.add(db_user)
        session.flush()
        session.refresh(db_user)
        return db_user
