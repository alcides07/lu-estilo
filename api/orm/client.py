from api.dependencies.get_session_db import SessionDep
from api.models.client import Client
from api.models.user import User
from api.schemas.client import ClientCreate
from api.orm.utils.get_object_or_404 import get_object_or_404
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from api.services.client import check_cpf_exists, check_user_client_exists
from api.filters.client import ClientFilter
from api.schemas.utils.pagination import PaginationSchema
from api.orm.utils.filter_collection import filter_collection


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
    db_client = Client(**client.model_dump())
    get_object_or_404(session, User, client.user_id, detail="Usuário não encontrado")
    check_cpf_exists(session, client.cpf)
    check_user_client_exists(session, client.user_id)

    try:
        session.add(db_client)
        session.commit()
        return db_client

    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Database error"
        )  # ENVIAR PARA LOG
