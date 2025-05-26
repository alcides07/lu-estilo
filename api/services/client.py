from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from filters.client import ClientFilter
from models.client import Client, check_user_client_exists
from models.user import User
from schemas.client import ClientCreate, ClientUpdate
from orm.utils.filter_collection import filter_collection
from orm.utils.get_object_or_404 import get_object_or_404
from schemas.utils.pagination import PaginationSchema
from sqlalchemy.exc import SQLAlchemyError


class ClientService:
    def __init__(self, session: Session):
        self.session = session

    async def read_client(self, client_id: int):
        client = get_object_or_404(
            self.session, Client, client_id, detail="Cliente não encontrado"
        )
        return client

    def list_clients(self, pagination: PaginationSchema, filters: ClientFilter):
        data, metadata = filter_collection(
            self.session,
            model=Client,
            pagination=pagination,
            filters=filters,
        )
        return data, metadata

    def create_client(self, client: ClientCreate) -> Client:
        get_object_or_404(
            self.session, User, client.user_id, detail="Usuário não encontrado"
        )
        db_client = Client(**client.model_dump())
        check_user_client_exists(self.session, client.user_id)

        try:
            self.session.add(db_client)
            self.session.commit()
            return db_client

        except SQLAlchemyError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Database error"
            )  # ENVIAR PARA LOG

    def update_client(self, client: ClientUpdate, id: int) -> Client:
        db_client = get_object_or_404(
            self.session, Client, id, detail="Cliente não encontrado"
        )

        for key, value in client:
            if value != None and hasattr(db_client, key):
                setattr(db_client, key, value)

        try:
            self.session.commit()
            self.session.refresh(db_client)

            return db_client

        except SQLAlchemyError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Database error"
            )  # ENVIAR PARA LOG

    async def delete_client(self, client_id: int):
        client = get_object_or_404(
            self.session, Client, client_id, detail="Cliente não encontrado"
        )

        try:
            self.session.delete(client)
            self.session.commit()

        except SQLAlchemyError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Database error"
            )  # ENVIAR PARA LOG
