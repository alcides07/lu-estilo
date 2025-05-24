from dependencies.get_session_db import SessionDep
from models.client import Client, check_user_client_exists
from models.user import User
from schemas.client import ClientCreate, ClientUpdate
from orm.utils.get_object_or_404 import get_object_or_404
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from filters.client import ClientFilter
from schemas.utils.pagination import PaginationSchema
from orm.utils.filter_collection import filter_collection


def read_client(session: SessionDep, client_id: int):
    client = get_object_or_404(session, Client, client_id)
    return client


def list_clients(
    session: SessionDep, pagination: PaginationSchema, filters: ClientFilter
):
    data = filter_collection(
        session,
        model=Client,
        pagination=pagination,
        filters=filters,
    )
    return data


def create_client(client: ClientCreate, session: SessionDep) -> Client:
    get_object_or_404(session, User, client.user_id, detail="Usuário não encontrado")
    db_client = Client(**client.model_dump())
    check_user_client_exists(session, client.user_id)

    try:
        session.add(db_client)
        session.commit()
        return db_client

    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Database error"
        )  # ENVIAR PARA LOG


def update_client(client: ClientUpdate, id: int, session: SessionDep) -> Client:
    db_client = get_object_or_404(session, Client, id, detail="Cliente não encontrado")

    for key, value in client:
        if value != None and hasattr(db_client, key):
            setattr(db_client, key, value)

    try:
        session.commit()
        session.refresh(db_client)

        return db_client

    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Database error"
        )  # ENVIAR PARA LOG


async def delete_client(client_id: int, session: SessionDep):
    client = get_object_or_404(
        session, Client, client_id, detail="Cliente não encontrado"
    )

    try:
        session.delete(client)
        session.commit()

    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Database error"
        )  # ENVIAR PARA LOG
