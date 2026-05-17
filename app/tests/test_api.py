import pytest
from fastapi.testclient import TestClient


@pytest.mark.usefixtures("test_db")
def test_create_user(client: TestClient) -> None:
    response = client.post(
        "/users",
        json={"username": "testuser", "password": "password123"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "testuser"
    assert data["id"] == user_id