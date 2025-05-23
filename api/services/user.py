from api.models.user import User
from api.orm.utils.exists import exists
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def check_email_exists(session: Session, email: str) -> bool:
    """Verifica se e-mail já está cadastrado"""
    if exists(
        session,
        User,
        email=email,
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Já existe um usuário com esse e-mail"
        )

    return False


def check_name_exists(session: Session, name: str) -> bool:
    """Verifica se name já está cadastrado"""
    if exists(
        session,
        User,
        name=name,
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Já existe um usuário com esse nome"
        )

    return False
