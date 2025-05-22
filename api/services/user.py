from api.models.user import User
from api.orm.utils.exists import exists
from sqlalchemy.orm import Session
from fastapi import HTTPException


def check_email_exists(session: Session, email: str) -> None:
    """Verifica se e-mail já está cadastrado"""
    if exists(
        session,
        User,
        email=email,
    ):
        raise HTTPException(400, "Já existe um usuário com esse e-mail")


def check_user_exists(session: Session, user_id: int) -> None:
    """Verifica se já existe um cliente vinculado ao usuário fornecido"""
    if exists(session, Client, user_id=user_id):
        raise HTTPException(400, "Já existe um cliente associado a esse usuário")
