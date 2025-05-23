from api.models.administrator import Administrator
from api.orm.utils.exists import exists
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def check_user_administrator_exists(session: Session, user_id: int) -> None:
    """Verifica se já existe um administrador vinculado ao usuário fornecido"""
    if exists(session, Administrator, user_id=user_id):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Já existe um administrador associado a esse usuário",
        )
