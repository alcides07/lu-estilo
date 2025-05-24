from sqlalchemy.orm import Session
from api.filters.category import CategoryFilter
from api.models.category import Category
from api.orm.utils.filter_collection import filter_collection
from api.orm.utils.get_object_or_404 import get_object_or_404
from api.schemas.category import CategoryCreate
from api.schemas.utils.pagination import PaginationSchema


class CategoryService:
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def validate_category_exists(session: Session, category_id: int) -> None:
        get_object_or_404(
            session, Category, category_id, detail="Categoria não encontrada"
        )

    def list_categories(self, pagination: PaginationSchema, filters: CategoryFilter):
        data = filter_collection(
            self.session,
            model=Category,
            pagination=pagination,
            filters=filters,
        )
        return data

    def create_category(self, category: CategoryCreate):
        new_category = Category(**category.model_dump())
        self.session.add(new_category)
        self.session.commit()
        self.session.refresh(new_category)

        return new_category
