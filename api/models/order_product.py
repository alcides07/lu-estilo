from sqlalchemy import UUID, ForeignKey
from database.config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from sqlalchemy.types import DECIMAL


class OrderProduct(Base):
    __tablename__ = "order_product"

    order_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("order.id", ondelete="CASCADE"),
        primary_key=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id", ondelete="RESTRICT"), primary_key=True
    )
    quantity: Mapped[int]
    unit_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    order: Mapped["Order"] = relationship("Order", back_populates="products")
    product: Mapped["Product"] = relationship("Product", back_populates="orders")
