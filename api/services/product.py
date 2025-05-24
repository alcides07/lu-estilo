from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from api.filters.product import ProductFilter
from api.models.product import Product
from api.orm.utils.get_object_or_404 import get_object_or_404
from api.orm.utils.filter_collection import filter_collection
from api.schemas.product import ProductCreate
from api.schemas.utils.pagination import PaginationSchema
from api.services.category import CategoryService
from sqlalchemy.exc import SQLAlchemyError


class ProductService:
    def __init__(self, session: Session):
        self.session = session

    def read_product(self, id):
        product = get_object_or_404(self.session, Product, id)
        return product

    def list_products(self, pagination: PaginationSchema, filters: ProductFilter):
        data = filter_collection(
            self.session,
            model=Product,
            pagination=pagination,
            filters=filters,
        )
        return data

    def create_product(self, product: ProductCreate):
        if product.category_id is not None:
            CategoryService.validate_category_exists(self.session, product.category_id)

        new_product = Product(**product.model_dump())

        try:
            self.session.add(new_product)
            self.session.commit()
            self.session.refresh(new_product)

        except SQLAlchemyError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Database error"
            )  # ENVIAR PARA LOG

        return new_product

    def update_product(self, id, data):
        db_product = get_object_or_404(
            self.session, Product, id, detail="Produto não encontrado"
        )

        for key, value in data:
            if value != None and hasattr(db_product, key):
                setattr(db_product, key, value)

        try:
            self.session.commit()
            self.session.refresh(db_product)

            return db_product

        except SQLAlchemyError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Database error"
            )  # ENVIAR PARA LOG

    async def delete_product(self, id):
        product = get_object_or_404(self.session, Product, id)

        try:
            self.session.delete(product)
            self.session.commit()

        except SQLAlchemyError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Database error"
            )  # ENVIAR PARA LOG
