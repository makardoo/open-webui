import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.apps.model import store as model_store
from backend.apps.auth import store as auth_store

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_data():
    model_store._store.clear()
    auth_store._store.clear()
    yield
    model_store._store.clear()
    auth_store._store.clear()


def _register_and_token(email="model@test.com", password="pass1234"):
    client.post("/auth/register", json={"email": email, "password": password, "name": "Tester"})
    resp = client.post("/auth/signin", json={"email": email, "password": password})
    return resp.json()["access_token"]


@pytest.fixture
def auth_headers():
    token = _register_and_token()
    return {"Authorization": f"Bearer {token}"}


def test_create_model(auth_headers):
    payload = {"name": "GPT-4", "provider": "openai", "model_id": "gpt-4", "description": "Advanced model"}
    resp = client.post("/models/", json=payload, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "GPT-4"
    assert data["provider"] == "openai"
    assert data["is_active"] is True


def test_list_models(auth_headers):
    client.post("/models/", json={"name": "M1", "provider": "openai", "model_id": "m1"}, headers=auth_headers)
    client.post("/models/", json={"name": "M2", "provider": "anthropic", "model_id": "m2"}, headers=auth_headers)
    resp = client.get("/models/", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_model(auth_headers):
    created = client.post("/models/", json={"name": "GPT-3", "provider": "openai", "model_id": "gpt-3"}, headers=auth_headers).json()
    resp = client.get(f"/models/{created['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_update_model(auth_headers):
    created = client.post("/models/", json={"name": "OldName", "provider": "openai", "model_id": "old"}, headers=auth_headers).json()
    resp = client.patch(f"/models/{created['id']}", json={"name": "NewName", "is_active": False}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "NewName"
    assert resp.json()["is_active"] is False


def test_delete_model(auth_headers):
    created = client.post("/models/", json={"name": "ToDelete", "provider": "openai", "model_id": "del"}, headers=auth_headers).json()
    resp = client.delete(f"/models/{created['id']}", headers=auth_headers)
    assert resp.status_code == 204
    resp = client.get(f"/models/{created['id']}", headers=auth_headers)
    assert resp.status_code == 404
