from sqladmin import ModelView
from models.category import Category


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name]
