from decimal import Decimal
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas.product import ProductRead
from schemas.order_product import OrderProductRead, ProductOfOrder
from models.order_product import OrderProduct
from models.order import Order
from services.product import ProductService
from models.user import User
from schemas.order import OrderCreate, OrderRead, OrderStatus
from sqlalchemy.exc import SQLAlchemyError


class OrderService:
    def __init__(self, session: Session):
        self.session = session

    async def list_orders(self) -> list[OrderProductRead]:

        stmt = select(Order)
        orders = self.session.execute(stmt).scalars().all()
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

        return response

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

            order_products = []
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

            order_response = OrderProductRead(
                order=OrderRead.model_validate(new_order),
                products=order_products,
            )

            return order_response

        except SQLAlchemyError:
            self.session.rollback()
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Database error"
            )  # ENVIAR PARA LOG

    # def update_product(self, id, data):
    #     db_product = get_object_or_404(
    #         self.session, Product, id, detail="Produto não encontrado"
    #     )

    #     for key, value in data:
    #         if value != None and hasattr(db_product, key):
    #             setattr(db_product, key, value)

    #     try:
    #         self.session.commit()
    #         self.session.refresh(db_product)

    #         return db_product

    #     except SQLAlchemyError:
    #         raise HTTPException(
    #             status.HTTP_400_BAD_REQUEST, detail="Database error"
    #         )  # ENVIAR PARA LOG

    # async def delete_product(self, id):
    #     product = get_object_or_404(self.session, Product, id)

    #     try:
    #         self.session.delete(product)
    #         self.session.commit()

    #     except SQLAlchemyError:
    #         raise HTTPException(
    #             status.HTTP_400_BAD_REQUEST, detail="Database error"
    #         )  # ENVIAR PARA LOG
