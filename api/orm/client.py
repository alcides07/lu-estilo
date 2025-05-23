from api.dependencies.get_session_db import SessionDep
from api.models.client import Client
from api.models.user import User
from api.schemas.client import ClientCreate
from api.orm.utils.get_object_or_404 import get_object_or_404
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from api.services.client import check_cpf_exists, check_user_exists


def create_client(client: ClientCreate, session: SessionDep) -> Client:
    db_client = Client(**client.model_dump())
    get_object_or_404(session, User, client.user_id, detail="Usuário não encontrado")
    check_cpf_exists(session, client.cpf)
    check_user_exists(session, client.user_id)

    try:
        session.add(db_client)
        session.commit()
        return db_client

    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Database error")  # ENVIAR PARA LOG
