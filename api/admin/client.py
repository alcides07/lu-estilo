from sqladmin import ModelView
from models.client import Client


class ClientAdmin(ModelView, model=Client):
    column_list = [Client.id, Client.cpf]
