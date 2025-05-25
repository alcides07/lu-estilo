from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from typing import List, Optional
from models.client import Client
from database.config import Base
from sqlalchemy import DECIMAL, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Order(Base):
    __tablename__ = "order"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    date: Mapped[datetime] = mapped_column(default=datetime.now, index=True)
    status: Mapped[str] = mapped_column(index=True)
    client_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("client.id", ondelete="SET NULL"), index=True
    )
    client: Mapped[Optional[Client]] = relationship(back_populates="orders")
    products: Mapped[List["OrderProduct"]] = relationship(back_populates="order")
    price_total: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))

    def __repr__(self) -> str:
        if self.client is not None:
            return f"{self.client} - {self.date}"

        return str(self.date)
