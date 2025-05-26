import pytest
from tests.factories.product import ProductFactory
from tests.factories.category import CategoryFactory
from schemas.category import CategoryCreate
from services.category import CategoryService
from main import app
from tests.utils.login import login
from schemas.administrator import AdministratorCreate
from schemas.client import ClientCreate
from schemas.user import UserCreate
from services.administrator import AdministratorService
from services.client import ClientService
from services.user import UserService
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from dependencies.get_session_db import get_session_db
from database.config import Base
from sqlalchemy import create_engine
from faker import Faker

fake = Faker("pt_BR")


@pytest.fixture(scope="session")
def engine():
    connect_args = {"check_same_thread": False}

    engine = create_engine("sqlite:///:memory:", connect_args=connect_args)
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture(autouse=True, scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True, scope="function")
def agent(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides = {}


@pytest.fixture
def client(db_session):
    user_service = UserService(db_session)
    client_service = ClientService(db_session)

    user = UserCreate(name="client", password="123", email="client@example.cm")
    new_user = user_service.create_user(user)

    cpf = fake.cpf().replace(".", "").replace("-", "")
    client_submit = ClientCreate(user_id=new_user.id, cpf=cpf)
    new_client = client_service.create_client(client_submit)

    access_token, refresh_token = login(new_client.user)
    agent = TestClient(app, headers={"Authorization": f"Bearer {access_token}"})

    return {
        "agent": agent,
        "user": new_user,
        "role": new_client,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "session": db_session,
    }


@pytest.fixture
def administrator(db_session):
    user_service = UserService(db_session)
    administrator_service = AdministratorService(db_session)

    user = UserCreate(name="admin", password="123", email="admin@example.cm")
    new_user = user_service.create_user(user)

    administrator_submit = AdministratorCreate(user_id=new_user.id)
    new_administrator = administrator_service.create_administrator(administrator_submit)

    access_token, refresh_token = login(new_administrator.user)
    agent = TestClient(app, headers={"Authorization": f"Bearer {access_token}"})

    return {
        "agent": agent,
        "user": new_user,
        "role": new_administrator,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "session": db_session,
    }


@pytest.fixture
def user(db_session):
    user_service = UserService(db_session)

    user = UserCreate(name="user", password="123", email="user@example.cm")

    new_user = user_service.create_user(user)
    access_token, refresh_token = login(new_user)
    agent = TestClient(app, headers={"Authorization": f"Bearer {access_token}"})

    return {
        "agent": agent,
        "user": new_user,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "session": db_session,
    }


@pytest.fixture
def product(db_session):
    category = CategoryFactory(session=db_session)
    product = ProductFactory(session=db_session, category=category)

    return product


@pytest.fixture
def category(db_session):
    category_service = CategoryService(db_session)
    category_submit = CategoryCreate(name="category", description="description")
    new_category = category_service.create_category(category=category_submit)

    return new_category
