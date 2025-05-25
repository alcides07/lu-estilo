from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from filters.product import ProductFilter
from models.product import Product
from orm.utils.get_object_or_404 import get_object_or_404
from orm.utils.filter_collection import filter_collection
from schemas.product import ProductCreate
from schemas.utils.pagination import PaginationSchema
from services.category import CategoryService
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select


class ProductService:
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def return_product_new_stock(product: Product, qtty_remove_stock: int) -> int:
        new_stock = product.stock - qtty_remove_stock

        return new_stock

    @staticmethod
    def validate_and_return_product_new_stock(
        product: Product, qtty_remove_stock: int
    ) -> int:
        new_stock = ProductService.return_product_new_stock(product, qtty_remove_stock)

        if new_stock < 0:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"O produto {product.description} possui {product.stock} unidades em estoque",
            )

        return new_stock

    async def read_product(self, id):
        product = get_object_or_404(self.session, Product, id)
        return product

    def list_products(self, pagination: PaginationSchema, filters: ProductFilter):
        data, metadata = filter_collection(
            self.session,
            model=Product,
            pagination=pagination,
            filters=filters,
        )
        return data, metadata

    async def list_products_by_ids(self, product_ids: list[int]) -> list[Product]:
        if not product_ids:
            return []

        stmt = select(Product).where(Product.id.in_(product_ids)).with_for_update()

        result = self.session.execute(stmt)
        products = result.scalars().all()

        found_ids = {p.id for p in products}
        missing_ids = set(product_ids) - found_ids

        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alguns produtos não foram encontrados: {', '.join(map(str, missing_ids))}",
            )

        return products

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
