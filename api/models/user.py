from ..database.config import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), index=True)
    password: Mapped[str] = mapped_column(String(length=32))
    email: Mapped[str] = mapped_column(String(length=255), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self) -> str:
        return f"{self.name} - {self.email}"
