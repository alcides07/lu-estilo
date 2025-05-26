from sqladmin import ModelView
from models.order_product import OrderProduct


class OrderProductAdmin(ModelView, model=OrderProduct):
    column_list = [
        OrderProduct.order_id,
        OrderProduct.product_id,
        OrderProduct.quantity,
    ]
