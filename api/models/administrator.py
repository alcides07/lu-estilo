from api.database.config import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


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
