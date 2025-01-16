import pytest
from fastapi.testclient import TestClient
from main import app
from tests.login_fixture import login_user

client = TestClient(app)


def test_create_call_plan(login_user):
    call_plan_data = {"restaurant_id": "24e3c305-e9b5-46f4-94b9-3d3d8aa0cff4", "user_id": "2b890904-0356-494c-afc4-7222f406ce85", "frequency_days": 30, "notes": "Follow up"}
    response = client.post("/v1/call-plans/", json=call_plan_data, headers={"Authorization": f"Bearer {login_user}"})
    assert response.status_code == 201
    assert "call_plan_id" in response.json()


def test_get_due_calls(login_user):
    response = client.get("/v1/call-plans/due-calls", headers={"Authorization": f"Bearer {login_user}"})
    assert response.status_code == 200
    assert "call_plans" in response.json()
