from api.database.config import Base
from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from fastapi import HTTPException, status
from sqlalchemy import event
from validate_docbr import CPF
from api.orm.utils.exists import exists


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(primary_key=True)
    cpf: Mapped[str] = mapped_column(String(length=11), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        unique=True,
    )
    user: Mapped["User"] = relationship(back_populates="client", single_parent=True)

    def __repr__(self) -> str:
        return f"{self.user.name} - {self.cpf}"


def check_client_cpf_exists(session: Session, cpf: str, exclude_id: int = None) -> bool:
    """Verifica se CPF já está cadastrado, excluindo um ID específico (para updates)"""
    query = select(Client).where(Client.cpf == cpf)
    if exclude_id is not None:
        query = query.where(Client.id != exclude_id)

    existing_client = session.execute(query).scalar_one_or_none()
    if existing_client:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Já existe um cliente com esse CPF"
        )
    return False


def check_user_client_exists(session: Session, user_id: int) -> bool:
    """Verifica se já existe um cliente vinculado ao usuário fornecido"""
    if exists(session, Client, user_id=user_id):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Já existe um cliente associado a esse usuário"
        )

    return False


def validate_cpf(cpf: str) -> bool:
    """Verifica se o CPF informado é válido"""

    cpf_obj = CPF()
    return cpf_obj.validate(cpf)


@event.listens_for(Client, "before_update")
@event.listens_for(Client, "before_insert")
def validate_client_cpf(mapper, connection, target):
    if not validate_cpf(target.cpf):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "CPF inválido")

    session = Session.object_session(target) or Session(bind=connection)
    exclude_id = target.id if hasattr(target, "id") else None

    check_client_cpf_exists(session, target.cpf, exclude_id)


@event.listens_for(Client, "before_insert")
def validate_user_client(mapper, connection, target):
    session = Session.object_session(target) or Session(bind=connection)

    check_user_client_exists(session, target.user_id)
