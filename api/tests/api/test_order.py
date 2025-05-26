import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from tests.factories.product import ProductFactory
from schemas.order_product import OrderProductRead
from schemas.order import OrderCreate, OrderStatus, ProductOrder
from fastapi import status


def perform_list_order(agent: TestClient, expected_status):
    response = agent.get("/orders/")
    assert response.status_code == expected_status


def perform_create_order(
    user_fixture,
    user_type,
    data: OrderCreate,
    expected_status: int,
):
    order_submit = jsonable_encoder(data)

    agent = user_fixture["agent"]
    role_id = user_fixture["role"].id

    response = agent.post(
        "/orders/",
        json=order_submit,
    )
    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        response_data = response.json()
        order_product_read = OrderProductRead.model_validate(response_data)

        assert order_product_read.order.id is not None
        assert order_product_read.order.date is not None
        assert order_product_read.order.status == OrderStatus.RECEIVED
        assert order_product_read.order.client is not None
        assert order_product_read.order.price_total is not None

        if user_type == "client":
            assert order_product_read.order.client.id == role_id


@pytest.mark.parametrize(
    "user_type,expected_status",
    [
        ("client", status.HTTP_403_FORBIDDEN),
        ("administrator", status.HTTP_200_OK),
    ],
)
def test_list_order(request, user_type, expected_status):
    user_fixture = request.getfixturevalue(user_type)
    perform_list_order(user_fixture["agent"], expected_status)


@pytest.mark.parametrize(
    "user_type,expected_status",
    [
        ("client", status.HTTP_200_OK),
        ("administrator", status.HTTP_200_OK),
    ],
)
def test_read_my_order(request, user_type, expected_status, db_session):
    user_fixture = request.getfixturevalue(user_type)

    product_1 = ProductFactory(session=db_session)
    product_order_1 = ProductOrder(id=product_1.id, quantity=1)
    products = [product_order_1]

    order_data = OrderCreate(products=products)

    perform_create_order(user_fixture, user_type, order_data, expected_status)


@pytest.mark.parametrize(
    "user_type,expected_status",
    [
        ("client", status.HTTP_201_CREATED),
        ("administrator", status.HTTP_403_FORBIDDEN),
    ],
)
def test_create_order(request, user_type, expected_status, db_session):
    user_fixture = request.getfixturevalue(user_type)

    product_1 = ProductFactory(session=db_session)
    product_2 = ProductFactory(session=db_session)

    product_order_1 = ProductOrder(id=product_1.id, quantity=1)
    product_order_2 = ProductOrder(id=product_2.id, quantity=1)

    products = [product_order_1, product_order_2]

    order_data = OrderCreate(products=products)

    perform_create_order(user_fixture, user_type, order_data, expected_status)
