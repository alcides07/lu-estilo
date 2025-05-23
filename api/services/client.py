from api.models.client import Client
from api.orm.utils.exists import exists
from sqlalchemy.orm import Session
from fastapi import HTTPException


def check_cpf_exists(session: Session, cpf: str) -> None:
    """Verifica se CPF já está cadastrado"""
    if exists(session, Client, cpf=cpf):
        raise HTTPException(400, "Já existe um cliente com esse CPF")


def check_user_exists(session: Session, user_id: int) -> None:
    """Verifica se já existe um cliente vinculado ao usuário fornecido"""
    if exists(session, Client, user_id=user_id):
        raise HTTPException(400, "Já existe um cliente associado a esse usuário")
