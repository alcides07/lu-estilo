from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from filters.administrator import AdministratorFilter
from models.administrator import Administrator
from models.user import User
from schemas.administrator import AdministratorCreate
from orm.utils.filter_collection import filter_collection
from orm.utils.get_object_or_404 import get_object_or_404
from schemas.utils.pagination import PaginationSchema
from sqlalchemy.exc import SQLAlchemyError


class AdministratorService:
    def __init__(self, session: Session):
        self.session = session

    def list_administrators(
        self, pagination: PaginationSchema, filters: AdministratorFilter
    ):
        data, metadata = filter_collection(
            self.session,
            model=Administrator,
            pagination=pagination,
            filters=filters,
        )
        return data, metadata

    def create_administrator(self, administrator: AdministratorCreate) -> Administrator:
        get_object_or_404(
            self.session, User, administrator.user_id, detail="Usuário não encontrado"
        )
        db_administrator = Administrator(**administrator.model_dump())

        try:
            self.session.add(db_administrator)
            self.session.commit()
            return db_administrator

        except SQLAlchemyError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Database error"
            )  # ENVIAR PARA LOG
