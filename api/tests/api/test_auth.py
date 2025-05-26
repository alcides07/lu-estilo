def test_refresh_token(client):
    refresh_token = client["refresh_token"]

    response = client["agent"].post(
        "/auth/refresh-token/", json={"refresh": refresh_token}
    )
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["access"] is not None
