from typing import List, Optional
from database.config import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[Optional[str]] = mapped_column(String(length=255))
    products: Mapped[List["Product"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"{self.name} - {self.description}"
