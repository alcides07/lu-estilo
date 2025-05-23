from api.models.client import Client
from api.orm.utils.exists import exists
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def check_cpf_exists(session: Session, cpf: str) -> bool:
    """Verifica se CPF já está cadastrado"""
    if exists(session, Client, cpf=cpf):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Já existe um cliente com esse CPF"
        )

    return False


def check_user_client_exists(session: Session, user_id: int) -> bool:
    """Verifica se já existe um cliente vinculado ao usuário fornecido"""
    if exists(session, Client, user_id=user_id):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Já existe um cliente associado a esse usuário"
        )

    return False
