from typing import Optional, List
from models.order_product import OrderProduct
from database.config import Base
from sqlalchemy import ForeignKey, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DECIMAL
from decimal import Decimal
from datetime import date


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(length=500))
    value: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), index=True)
    bar_code: Mapped[str]
    stock: Mapped[int] = mapped_column(index=True)
    expiration_date: Mapped[Optional[date]]
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("category.id", ondelete="SET NULL"), index=True
    )
    category: Mapped[Optional["Category"]] = relationship(back_populates="products")
    orders: Mapped[List[OrderProduct]] = relationship(back_populates="product")

    def __repr__(self) -> str:
        return self.description

    __table_args__ = (CheckConstraint("stock >= 0", name="stock_gte"),)
    __table_args__ = (CheckConstraint("value >= 0", name="value_gte"),)
