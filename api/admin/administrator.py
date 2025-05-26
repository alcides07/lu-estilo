from sqladmin import ModelView
from models.administrator import Administrator


class AdministratorAdmin(ModelView, model=Administrator):
    column_list = [Administrator.id]
