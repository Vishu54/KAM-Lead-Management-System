import pytest
from fastapi.testclient import TestClient
from main import app
from tests.login_fixture import login_user

client = TestClient(app)


@pytest.fixture
def test_create_restaurant(login_user):
    restaurant_data = {"name": "Test Restaurant", "address": "123 Test St", "phone": "+1234567890", "email": "test@restaurant.com"}
    response = client.post("/v1/restaurants/", json=restaurant_data, headers={"Authorization": f"Bearer {login_user}"})
    assert response.status_code == 201
    assert "restaurant_id" in response.json()
    return response.json()["restaurant_id"]


def test_get_restaurant(login_user, test_create_restaurant):
    response = client.get(f"/v1/restaurants/{test_create_restaurant}", headers={"Authorization": f"Bearer {login_user}"})
    assert response.status_code == 200
    assert "name" in response.json()
