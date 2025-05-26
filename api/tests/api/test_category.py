import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from faker import Faker
from schemas.category import CategoryCreate, CategoryRead
from fastapi import status

fake = Faker("pt_BR")


def perform_list_category(agent: TestClient, expected_status):
    response = agent.get("/categories/")
    assert response.status_code == expected_status


def perform_create_category(
    agent: TestClient, expected_status, category: CategoryCreate
):
    category_submit = jsonable_encoder(category)

    response = agent.post("/categories/", json=category_submit)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        response_data = response.json()
        category_read = CategoryRead.model_validate(response_data)

        assert category_read.id is not None
        assert category_read.name == category.name
        assert category_read.description == category.description


@pytest.mark.parametrize(
    "user_type,expected_status",
    [
        ("client", status.HTTP_200_OK),
        ("administrator", status.HTTP_200_OK),
    ],
)
def test_list_category(request, user_type, expected_status):
    user_fixture = request.getfixturevalue(user_type)
    perform_list_category(user_fixture["agent"], expected_status)


@pytest.mark.parametrize(
    "user_type,expected_status",
    [
        ("client", status.HTTP_403_FORBIDDEN),
        ("administrator", status.HTTP_201_CREATED),
    ],
)
def test_create_category(request, user_type, expected_status, db_session):
    user_fixture = request.getfixturevalue(user_type)

    category = CategoryCreate(name="category", description="description")

    perform_create_category(user_fixture["agent"], expected_status, category)
