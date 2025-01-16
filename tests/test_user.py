import pytest
from fastapi.testclient import TestClient
from tests.login_fixture import login_user
from main import app

client = TestClient(app)


def test_create_user(login_user):
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "+1234567890",
        "role": "Staff",
        "restaurant_id": "24e3c305-e9b5-46f4-94b9-3d3d8aa0cff4",
        "password": "password",
    }
    response = client.post("/v1/auth/register/", json=user_data, headers={"Authorization": f"Bearer {login_user}"})
    assert response.status_code == 201
    assert "user_id" in response.json()


def test_get_user(login_user):
    response = client.get("/v1/user/2b890904-0356-494c-afc4-7222f406ce85", headers={"Authorization": f"Bearer {login_user}"})
    assert response.status_code == 200
    assert "name" in response.json()
