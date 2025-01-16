import pytest
from fastapi.testclient import TestClient
from main import app
from tests.login_fixture import login_user


client = TestClient(app)


def test_place_order(login_user):
    order_data = {"restaurant_id": "24e3c305-e9b5-46f4-94b9-3d3d8aa0cff4", "user_id": "2b890904-0356-494c-afc4-7222f406ce85", "amount": 1000, "notes": "Test order"}
    response = client.post("/v1/orders/", json=order_data, headers={"Authorization": f"Bearer {login_user}"})
    assert response.status_code == 201
    assert "order_id" in response.json()


def test_get_restaurant_orders(login_user):
    response = client.get("/v1/orders/restaurants/24e3c305-e9b5-46f4-94b9-3d3d8aa0cff4", headers={"Authorization": f"Bearer {login_user}"})
    assert response.status_code == 200
    assert isinstance(response.json()["orders"], list)
