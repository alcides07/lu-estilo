import pytest
from fastapi.testclient import TestClient
from faker import Faker
from tests.utils.login import login
from schemas.administrator import (
    AdministratorRead,
)
from services.user import UserService
from schemas.user import UserCreate
from fastapi import status

fake = Faker("pt_BR")


def perform_list_administrator(agent: TestClient, expected_status):
    response = agent.get("/administrators/")
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "user_type,expected_status",
    [
        ("client", status.HTTP_403_FORBIDDEN),
        ("administrator", status.HTTP_200_OK),
    ],
)
def test_list_administrator(request, user_type, expected_status):
    user_fixture = request.getfixturevalue(user_type)
    perform_list_administrator(user_fixture["agent"], expected_status)


def test_create_administrator(agent, db_session):
    user_service = UserService(db_session)
    user = UserCreate(
        name="administrator", password="123", email="administrator@example.cm"
    )
    new_user = user_service.create_user(user)

    access_token, _ = login(new_user)

    response = agent.post(
        "/administrators/",
        json={"user_id": new_user.id},
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 201

    response_data = response.json()
    administrator_read = AdministratorRead.model_validate(response_data)

    assert administrator_read.id is not None
    assert administrator_read.user.id == new_user.id
