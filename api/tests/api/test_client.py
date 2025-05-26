import pytest
from fastapi.testclient import TestClient
from faker import Faker
from services.client import ClientService
from schemas.client import ClientCreate, ClientRead
from services.user import UserService
from schemas.user import UserCreate
from fastapi.encoders import jsonable_encoder
from fastapi import status

fake = Faker("pt_BR")


def perform_list_client(agent: TestClient, expected_status):
    response = agent.get("/clients/")
    assert response.status_code == expected_status


def perform_read_my_client(agent: TestClient, expected_status, client_id, db_session):
    response = agent.get(f"/clients/{client_id}/")
    assert response.status_code == expected_status

    response_data = response.json()["data"]
    client_read = ClientRead.model_validate(response_data)

    if expected_status == status.HTTP_200_OK:
        assert client_read.id is not None


def perform_read_other_client(agent: TestClient, client_id: int):
    response = agent.get(f"/clients/{client_id}/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def perform_create_client(agent: TestClient, data: ClientCreate, expected_status: int):
    client_submit = jsonable_encoder(data)

    response = agent.post(
        "/clients/",
        json=client_submit,
    )
    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        response_data = response.json()
        client_read = ClientRead.model_validate(response_data)

        assert client_read.id is not None
        assert client_read.cpf == data.cpf


def test_read_my_client(client):
    perform_read_my_client(
        client["agent"],
        status.HTTP_200_OK,
        client["role"].id,
        client["session"],
    )


def test_read_other_client(client, db_session):
    user_service = UserService(session=db_session)
    client_service = ClientService(session=db_session)

    new_user_data = UserCreate(
        name="new_user", password="123", email="new_user@email.com"
    )
    new_user_obj = user_service.create_user(new_user_data)

    cpf = fake.cpf().replace(".", "").replace("-", "")
    new_client_data = ClientCreate(user_id=new_user_obj.id, cpf=cpf)
    new_client_obj = client_service.create_client(client=new_client_data)

    perform_read_other_client(client["agent"], new_client_obj.id)


@pytest.mark.parametrize(
    "user_type,expected_status",
    [
        ("client", status.HTTP_403_FORBIDDEN),
        ("administrator", status.HTTP_200_OK),
    ],
)
def test_list_client(request, user_type, expected_status):
    user_fixture = request.getfixturevalue(user_type)
    perform_list_client(user_fixture["agent"], expected_status)


def test_create_client(user):
    cpf = fake.cpf().replace(".", "").replace("-", "")
    client_data = ClientCreate(user_id=user["user"].id, cpf=cpf)

    perform_create_client(user["agent"], client_data, status.HTTP_201_CREATED)


def test_delete_my_client(client):
    client_id = client["role"].id
    response = client["agent"].delete(f"/clients/{client_id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_other_client(client, db_session):
    user_service = UserService(session=db_session)
    client_service = ClientService(session=db_session)

    new_user_data = UserCreate(
        name="new_user", password="123", email="new_user@email.com"
    )
    new_user_obj = user_service.create_user(new_user_data)

    cpf = fake.cpf().replace(".", "").replace("-", "")
    new_client_data = ClientCreate(user_id=new_user_obj.id, cpf=cpf)
    new_client_obj_id = client_service.create_client(client=new_client_data).id

    response = client["agent"].delete(f"/clients/{new_client_obj_id}/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_my_client(client):
    old_cpf = client["role"].cpf
    client_id = client["role"].id

    new_cpf = fake.cpf().replace(".", "").replace("-", "")
    new_data = {"cpf": new_cpf}

    response = client["agent"].put(
        f"/clients/{client_id}/",
        json=new_data,
    )
    assert response.status_code == 200
    response_data = response.json()

    assert response_data["cpf"] == new_cpf
    assert response_data["cpf"] != old_cpf


def test_update_other_client(client, db_session):
    user_service = UserService(session=db_session)
    client_service = ClientService(session=db_session)

    new_user_data = UserCreate(
        name="new_user", password="123", email="new_user@email.com"
    )
    new_user_obj = user_service.create_user(new_user_data)

    cpf = fake.cpf().replace(".", "").replace("-", "")
    new_client_data = ClientCreate(user_id=new_user_obj.id, cpf=cpf)
    new_client_obj_id = client_service.create_client(client=new_client_data).id

    new_cpf = fake.cpf().replace(".", "").replace("-", "")
    new_data = {"cpf": new_cpf}

    response = client["agent"].put(
        f"/clients/{new_client_obj_id}/",
        json=new_data,
    )
    assert response.status_code == 403
