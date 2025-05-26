from fastapi.testclient import TestClient
from main import app

agent = TestClient(app)


def login(user):
    login_data = {"username": user.name, "password": "123"}

    response = agent.post("/auth/login/", data=login_data)
    assert response.status_code == 200

    response_data = response.json()

    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]

    assert access_token is not None
    assert refresh_token is not None

    return access_token, refresh_token
