import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from decimal import Decimal
from models.product import Product

fake = Faker()


class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    description = factory.LazyAttribute(lambda x: fake.unique.catch_phrase())
    value = factory.LazyAttribute(
        lambda x: Decimal(
            str(round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2))
        )
    )
    bar_code = factory.LazyAttribute(lambda x: fake.unique.ean13())
    stock = factory.LazyAttribute(lambda x: fake.random_int(min=1, max=1000))
    expiration_date = factory.LazyAttribute(
        lambda x: fake.date_between(start_date="+30d", end_date="+5y")
    )

    category_id = None

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop("session", None)
        category = kwargs.pop("category", None)

        if session is not None:
            cls._meta.sqlalchemy_session = session

        if category is not None:
            kwargs["category_id"] = category.id

        return super()._create(model_class, *args, **kwargs)
