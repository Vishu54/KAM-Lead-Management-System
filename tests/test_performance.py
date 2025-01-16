import pytest
from fastapi.testclient import TestClient
from main import app
from tests.login_fixture import login_user

client = TestClient(app)


def test_generate_metrics(login_user):
    response = client.post(
        "/v1/performance/restaurants/24e3c305-e9b5-46f4-94b9-3d3d8aa0cff4/metrics", params={"year": 2023, "month": 1}, headers={"Authorization": f"Bearer {login_user}"}
    )
    assert response.status_code == 200
    assert "metric_id" in response.json()


def test_get_restaurant_metrics(login_user):
    response = client.get("/v1/performance/restaurants/24e3c305-e9b5-46f4-94b9-3d3d8aa0cff4/metrics", headers={"Authorization": f"Bearer {login_user}"})
    assert response.status_code == 200
    assert "metrics" in response.json()
