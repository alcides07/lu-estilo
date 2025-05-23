from api.models.user import User
from api.orm.utils.exists import exists
from sqlalchemy.orm import Session
from fastapi import HTTPException


def check_email_exists(session: Session, email: str) -> bool:
    """Verifica se e-mail já está cadastrado"""
    if exists(
        session,
        User,
        email=email,
    ):
        raise HTTPException(400, "Já existe um usuário com esse e-mail")

    return False


def check_name_exists(session: Session, name: str) -> bool:
    """Verifica se name já está cadastrado"""
    if exists(
        session,
        User,
        name=name,
    ):
        raise HTTPException(400, "Já existe um usuário com esse nome")

    return False
