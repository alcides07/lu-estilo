from sqladmin import ModelView
from models.order import Order


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.date, Order.status, Order.price_total]
