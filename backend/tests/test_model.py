import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.apps.model.store import clear_all_models
from backend.apps.auth.store import clear_all_users

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_data():
    clear_all_models()
    clear_all_users()
    yield
    clear_all_models()
    clear_all_users()


def _register_and_token(email="model_user@example.com", password="secret"):
    client.post("/auth/register", json={"email": email, "password": password, "name": "Model User"})
    resp = client.post("/auth/signin", json={"email": email, "password": password})
    return resp.json()["token"]


@pytest.fixture
def auth_headers():
    token = _register_and_token()
    return {"Authorization": f"Bearer {token}"}


def test_create_model(auth_headers):
    resp = client.post("/models/", json={"name": "my-model", "base_model": "gpt-4", "system_prompt": "You are helpful."}, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "my-model"
    assert data["base_model"] == "gpt-4"


def test_list_models(auth_headers):
    client.post("/models/", json={"name": "m1", "base_model": "gpt-3.5"}, headers=auth_headers)
    client.post("/models/", json={"name": "m2", "base_model": "gpt-4"}, headers=auth_headers)
    resp = client.get("/models/", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_model(auth_headers):
    created = client.post("/models/", json={"name": "fetch-model", "base_model": "llama"}, headers=auth_headers).json()
    resp = client.get(f"/models/{created['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_update_model(auth_headers):
    created = client.post("/models/", json={"name": "old-name", "base_model": "gpt-4"}, headers=auth_headers).json()
    resp = client.put(f"/models/{created['id']}", json={"name": "new-name"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "new-name"


def test_delete_model(auth_headers):
    created = client.post("/models/", json={"name": "to-delete", "base_model": "gpt-4"}, headers=auth_headers).json()
    resp = client.delete(f"/models/{created['id']}", headers=auth_headers)
    assert resp.status_code == 200
    get_resp = client.get(f"/models/{created['id']}", headers=auth_headers)
    assert get_resp.status_code == 404
