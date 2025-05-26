import pytest
from datetime import datetime
from decimal import Decimal
from fastapi.testclient import TestClient
from faker import Faker
from schemas.category import CategoryCreate
from services.category import CategoryService
from schemas.product import ProductCreate, ProductRead, ProductUpdate
from fastapi.encoders import jsonable_encoder
from fastapi import status

fake = Faker("pt_BR")


def perform_list_product(agent: TestClient, expected_status):
    response = agent.get("/products/")
    assert response.status_code == expected_status


def perform_create_product(agent: TestClient, expected_status, product: ProductCreate):
    product_submit = jsonable_encoder(product)

    response = agent.post("/products/", json=product_submit)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        response_data = response.json()
        product_read = ProductRead.model_validate(response_data)

        assert product_read.id is not None
        assert product_read.description == product.description
        assert product_read.value == product.value
        assert product_read.bar_code == product.bar_code
        assert product_read.stock == product.stock

        if product_read.expiration_date:
            assert product_read.expiration_date == product.expiration_date

        if product_read.category:
            assert product_read.category.id == product.category_id

    return response


def perform_delete_product(agent: TestClient, expected_status, product_id):
    response = agent.delete(f"/products/{product_id}/")
    assert response.status_code == expected_status


def perform_update_product(
    agent: TestClient,
    expected_status,
    product_id,
    new_data: ProductUpdate,
):
    product_submit = jsonable_encoder(new_data)

    response = agent.put(
        f"/products/{product_id}/",
        json=product_submit,
    )
    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        response_data = response.json()
        product_read = ProductRead.model_validate(response_data)

        assert product_read.bar_code == new_data.bar_code
        assert product_read.value == new_data.value
        assert product_read.stock == new_data.stock

        if product_read.expiration_date:
            assert product_read.expiration_date == new_data.expiration_date

        if product_read.category:
            assert product_read.category.id == new_data.category_id


def perform_read_product(agent: TestClient, expected_status, product_id):
    response = agent.get(f"/products/{product_id}/")
    assert response.status_code == expected_status

    response_data = response.json()["data"]
    product_read = ProductRead.model_validate(response_data)

    if expected_status == status.HTTP_200_OK:
        assert product_read.id is not None


@pytest.mark.parametrize(
    "user_type,expected_status",
    [
        ("client", status.HTTP_200_OK),
        ("administrator", status.HTTP_200_OK),
    ],
)
def test_list_product(request, user_type, expected_status):
    user_fixture = request.getfixturevalue(user_type)
    perform_list_product(user_fixture["agent"], expected_status)


@pytest.mark.parametrize(
    "user_type,expected_status",
    [
        ("client", status.HTTP_200_OK),
        ("administrator", status.HTTP_200_OK),
    ],
)
def test_read_product(request, product, user_type, expected_status):
    user_fixture = request.getfixturevalue(user_type)
    perform_read_product(
        user_fixture["agent"],
        expected_status,
        product.id,
    )


@pytest.mark.parametrize(
    "user_type,expected_status",
    [
        ("client", status.HTTP_403_FORBIDDEN),
        ("administrator", status.HTTP_201_CREATED),
    ],
)
def test_create_product_only_with_required_fields(request, user_type, expected_status):
    user_fixture = request.getfixturevalue(user_type)
    product = ProductCreate(
        description="product", value=Decimal(5), bar_code="string", stock=5
    )

    perform_create_product(user_fixture["agent"], expected_status, product)


def test_create_product_complete_with_administrator(administrator, db_session):
    category_service = CategoryService(db_session)
    category_submit = CategoryCreate(name="category", description="description")
    category_obj = category_service.create_category(category=category_submit)

    product = ProductCreate(
        description="product",
        value=Decimal(5),
        bar_code="string",
        stock=5,
        category_id=category_obj.id,
        expiration_date=datetime(2025, 5, 26, 0, 0, 0),
    )

    perform_create_product(administrator["agent"], status.HTTP_201_CREATED, product)


@pytest.mark.parametrize(
    "user_type,expected_status",
    [
        ("client", status.HTTP_403_FORBIDDEN),
        ("administrator", status.HTTP_200_OK),
    ],
)
def test_update_product(request, category, product, user_type, expected_status):
    user_fixture = request.getfixturevalue(user_type)

    new_data = ProductUpdate(
        description="product",
        value=Decimal(5),
        bar_code="string",
        stock=5,
        category_id=category.id,
        expiration_date=datetime(2025, 5, 26, 0, 0, 0),
    )

    perform_update_product(user_fixture["agent"], expected_status, product.id, new_data)


@pytest.mark.parametrize(
    "user_type,expected_status",
    [
        ("client", status.HTTP_403_FORBIDDEN),
        ("administrator", status.HTTP_204_NO_CONTENT),
    ],
)
def test_delete_product(request, user_type, product, expected_status):
    user_fixture = request.getfixturevalue(user_type)

    perform_delete_product(user_fixture["agent"], expected_status, product.id)
