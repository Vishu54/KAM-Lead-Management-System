import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


@pytest.fixture
def login_user():
    response = client.post("/v1/auth/login", data={"username": "kfc_user1@email.com", "password": "admin"})
    return response.json()["access_token"]
