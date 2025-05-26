from decimal import Decimal
from typing import List, Tuple
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import Date, cast, desc, select
from sqlalchemy.orm import Session
from models.product import Product
from filters.order import OrderFilter
from schemas.utils.pagination import MetadataPagination, PaginationSchema
from orm.utils.count_collection import count_collection
from orm.utils.get_object_or_404 import get_object_or_404
from schemas.product import ProductRead
from schemas.order_product import OrderProductRead, ProductOfOrder
from models.order_product import OrderProduct
from models.order import Order
from services.product import ProductService
from models.user import User
from schemas.order import OrderCreate, OrderRead, OrderStatus, OrderUpdate
from sqlalchemy.exc import SQLAlchemyError


class OrderService:
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def apply_filters_orders(stmt, filters: OrderFilter):
        if filters.date__lte is not None:
            stmt = stmt.where(cast(Order.date, Date) <= filters.date__lte)

        if filters.date__gte is not None:
            stmt = stmt.where(cast(Order.date, Date) >= filters.date__gte)

        if filters.status is not None:
            stmt = stmt.where(Order.status == filters.status)

        if filters.client_id is not None:
            stmt = stmt.where(Order.client_id == filters.client_id)

        if filters.category_id is not None:
            stmt = (
                stmt.join(Order.products)
                .join(OrderProduct.product)
                .where(Product.category_id == filters.category_id)
            )

        return stmt

    async def get_products_of_order(
        self, orders: List[Order]
    ) -> Tuple[list[OrderProductRead], MetadataPagination]:
        response: List[OrderProductRead] = []
        for order in orders:
            products_list = [
                ProductOfOrder(
                    product=ProductRead.model_validate(product.product),
                    unit_price=product.unit_price,
                    quantity=product.quantity,
                )
                for product in order.products
            ]

            order_response = OrderProductRead(
                order=OrderRead.model_validate(order),
                products=products_list,
            )
            response.append(order_response)

        total_count = count_collection(self.session, Order)
        metadata = MetadataPagination(count=total_count)

        return response, metadata

    async def read_order(self, order_id: UUID) -> OrderProductRead:
        order = get_object_or_404(
            self.session, Order, order_id, detail="Pedido não encontrado"
        )
        result, _ = await self.get_products_of_order([order])
        return result[0]

    async def list_orders(
        self, pagination: PaginationSchema, filters: OrderFilter
    ) -> Tuple[list[OrderProductRead], MetadataPagination]:
        stmt = select(Order).order_by(desc(Order.date))

        stmt = OrderService.apply_filters_orders(stmt, filters)
        stmt = stmt.offset(pagination.offset).limit(pagination.limit)

        orders = self.session.execute(stmt).scalars().all()

        result, metadata = await self.get_products_of_order(orders)
        return result, metadata

    async def create_order(self, order: OrderCreate, user: User):
        product_ids = [p.id for p in order.products]
        product_service = ProductService(self.session)
        products = await product_service.list_products_by_ids(product_ids)

        products_dict = {p.id: p for p in products}

        for product_order in order.products:
            product = products_dict[product_order.id]
            product_service.validate_and_return_product_new_stock(
                product, product_order.quantity
            )

        try:
            new_order = Order(
                status=OrderStatus.RECEIVED,
                client_id=user.client.id,
                price_total=Decimal(0),
            )
            self.session.add(new_order)
            self.session.flush()

            order_products: List[OrderProduct] = []
            for product_order in order.products:
                product = products_dict[product_order.id]

                order_product = OrderProduct(
                    order_id=new_order.id,
                    product_id=product.id,
                    quantity=product_order.quantity,
                    unit_price=product.value,
                )
                order_products.append(order_product)

            order_price_total = Decimal(0)
            for product_order in order.products:
                product = products_dict[product_order.id]

                product.stock = product_service.return_product_new_stock(
                    product, product_order.quantity
                )
                order_price_total += product.value * (product_order.quantity)

            new_order.price_total = order_price_total

            self.session.add_all(order_products)
            self.session.commit()
            self.session.refresh(new_order)

            products_of_order: List[ProductOfOrder] = [
                ProductOfOrder(
                    product=op.product,
                    unit_price=op.unit_price,
                    quantity=op.quantity,
                )
                for op in order_products
            ]

            order_response = OrderProductRead(
                order=OrderRead.model_validate(new_order),
                products=products_of_order,
            )

            return order_response

        except SQLAlchemyError:
            self.session.rollback()
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Database error"
            )  # ENVIAR PARA LOG

    async def update_order(self, id, data: OrderUpdate) -> Order:
        db_order = get_object_or_404(
            self.session, Order, id, detail="Pedido não encontrado"
        )

        db_order.status = data.status

        try:
            self.session.commit()
            self.session.refresh(db_order)

            return db_order

        except SQLAlchemyError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Database error"
            )  # ENVIAR PARA LOG

    async def delete_order(self, id):
        order = get_object_or_404(self.session, Order, id)

        try:
            self.session.delete(order)
            self.session.commit()

        except SQLAlchemyError:
            self.session.rollback()
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Database error"
            )  # ENVIAR PARA LOG
