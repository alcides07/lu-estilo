from api.database.config import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(length=32))
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
