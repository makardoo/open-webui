import pytest
from fastapi.testclient import TestClient

from main import app
from apps.tag import store as tag_store
from apps.auth import store as auth_store

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_data():
    tag_store._tags.clear()
    auth_store._users.clear()
    yield
    tag_store._tags.clear()
    auth_store._users.clear()


def _register_and_token(email="tag@example.com", password="secret"):
    client.post("/auth/register", json={"email": email, "password": password, "name": "Tagger"})
    resp = client.post("/auth/signin", json={"email": email, "password": password})
    return resp.json()["access_token"]


@pytest.fixture
def auth_headers():
    token = _register_and_token()
    return {"Authorization": f"Bearer {token}"}


def test_create_tag(auth_headers):
    resp = client.post("/tags/", json={"name": "important", "color": "#ff0000"}, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "important"
    assert data["color"] == "#ff0000"
    assert "id" in data


def test_list_tags(auth_headers):
    client.post("/tags/", json={"name": "work"}, headers=auth_headers)
    client.post("/tags/", json={"name": "personal"}, headers=auth_headers)
    resp = client.get("/tags/", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_tag(auth_headers):
    created = client.post("/tags/", json={"name": "test"}, headers=auth_headers).json()
    resp = client.get(f"/tags/{created['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "test"


def test_update_tag(auth_headers):
    created = client.post("/tags/", json={"name": "old"}, headers=auth_headers).json()
    resp = client.put(f"/tags/{created['id']}", json={"name": "new", "color": "#00ff00"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "new"
    assert resp.json()["color"] == "#00ff00"


def test_delete_tag(auth_headers):
    created = client.post("/tags/", json={"name": "temp"}, headers=auth_headers).json()
    resp = client.delete(f"/tags/{created['id']}", headers=auth_headers)
    assert resp.status_code == 204
    get_resp = client.get(f"/tags/{created['id']}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_get_tag_not_found(auth_headers):
    resp = client.get("/tags/nonexistent-id", headers=auth_headers)
    assert resp.status_code == 404
