from api.database.config import Base
from fastapi import HTTPException, status
from sqlalchemy import ForeignKey, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from api.orm.utils.exists import exists


class Administrator(Base):
    __tablename__ = "administrator"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        unique=True,
    )
    user: Mapped["User"] = relationship(
        back_populates="administrator", single_parent=True
    )

    def __repr__(self) -> str:
        return self.user.name


def check_user_administrator_exists(session: Session, user_id: int) -> None:
    """Verifica se já existe um administrador vinculado ao usuário fornecido"""
    if exists(session, Administrator, user_id=user_id):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Já existe um administrador associado a esse usuário",
        )


@event.listens_for(Administrator, "before_insert")
def validate_user_administrator(mapper, connection, target):
    session = Session.object_session(target) or Session(bind=connection)

    check_user_administrator_exists(session, target.user_id)
