from database.config import Base
from sqlalchemy import String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from datetime import datetime
from orm.utils.exists import exists
from fastapi import HTTPException, status


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(length=255))
    email: Mapped[str] = mapped_column(String(length=255), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    client: Mapped["Client"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    administrator: Mapped["Administrator"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.name} - {self.email}"


def check_user_email_exists(session: Session, email: str) -> bool:
    """Verifica se e-mail já está cadastrado"""
    if exists(
        session,
        User,
        email=email,
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Já existe um usuário com esse e-mail"
        )

    return False


def check_name_exists(session: Session, name: str) -> bool:
    """Verifica se name já está cadastrado"""
    if exists(
        session,
        User,
        name=name,
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Já existe um usuário com esse nome"
        )

    return False


@event.listens_for(User, "before_insert")
@event.listens_for(User, "before_update")
def validate_user_email(mapper, connection, target):
    session = Session.object_session(target) or Session(bind=connection)
    check_user_email_exists(session, target.email)


@event.listens_for(User, "before_insert")
@event.listens_for(User, "before_update")
def validate_user_name(mapper, connection, target):
    session = Session.object_session(target) or Session(bind=connection)
    check_name_exists(session, target.name)
