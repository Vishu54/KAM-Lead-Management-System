import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_login_success():
    response = client.post("/v1/auth/login", data={"username": "kfc_user1@email.com", "password": "admin"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure():
    response = client.post("/v1/auth/login", data={"username": "wrong@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
