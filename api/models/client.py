from api.database.config import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi import HTTPException, status
from sqlalchemy import event
from validate_docbr import CPF


def validate_cpf(cpf: str) -> bool:
    """Verifica se o CPF informado é válido"""

    cpf_obj = CPF()
    return cpf_obj.validate(cpf)


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


@event.listens_for(Client, "before_insert")
def validate_client_cpf(mapper, connection, target):
    if not validate_cpf(target.cpf):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "CPF inválido")
