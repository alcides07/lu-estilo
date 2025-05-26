from factory.alchemy import SQLAlchemyModelFactory
import factory
from faker import Faker
from models.category import Category

fake = Faker()


class CategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    name = factory.LazyAttribute(
        lambda x: fake.unique.word().capitalize() + " Category"
    )
    description = factory.LazyAttribute(lambda x: fake.sentence(nb_words=6))

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop("session", None)

        if session is not None:
            cls._meta.sqlalchemy_session = session

        return super()._create(model_class, *args, **kwargs)
