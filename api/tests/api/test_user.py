from fastapi.testclient import TestClient
from schemas.user import UserCreate, UserRead
from fastapi.encoders import jsonable_encoder
from main import app

agent = TestClient(app)


def test_create_user():
    user_schema = UserCreate(name="test", password="123", email="email@domain.com")
    user_submit = jsonable_encoder(user_schema)

    response = agent.post("/auth/register/", json=user_submit)

    assert response.status_code == 201

    response_data = response.json()
    user_read = UserRead.model_validate(response_data)

    assert user_read.id is not None
    assert user_read.created_at is not None
    assert user_read.updated_at is not None
    assert user_read.name == user_schema.name
    assert user_read.email == user_schema.email
    assert not hasattr(user_read, "password")
