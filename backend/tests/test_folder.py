import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.apps.folder import store as folder_store
from backend.apps.auth import store as auth_store

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_data():
    folder_store.clear_all()
    auth_store.clear_all()
    yield
    folder_store.clear_all()
    auth_store.clear_all()


def _register_and_token(email="folder@test.com", password="pass123"):
    client.post("/auth/register", json={"email": email, "password": password, "name": "Tester"})
    resp = client.post("/auth/signin", json={"email": email, "password": password})
    return resp.json()["token"]


@pytest.fixture
def auth_headers():
    token = _register_and_token()
    return {"Authorization": f"Bearer {token}"}


def test_create_folder(auth_headers):
    resp = client.post("/folders/", json={"name": "My Folder"}, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "My Folder"
    assert data["parent_id"] is None


def test_list_folders(auth_headers):
    client.post("/folders/", json={"name": "A"}, headers=auth_headers)
    client.post("/folders/", json={"name": "B"}, headers=auth_headers)
    resp = client.get("/folders/", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_folder(auth_headers):
    created = client.post("/folders/", json={"name": "X"}, headers=auth_headers).json()
    resp = client.get(f"/folders/{created['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_update_folder(auth_headers):
    created = client.post("/folders/", json={"name": "Old"}, headers=auth_headers).json()
    resp = client.patch(f"/folders/{created['id']}", json={"name": "New"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "New"


def test_delete_folder(auth_headers):
    created = client.post("/folders/", json={"name": "Del"}, headers=auth_headers).json()
    resp = client.delete(f"/folders/{created['id']}", headers=auth_headers)
    assert resp.status_code == 204
    get_resp = client.get(f"/folders/{created['id']}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_nested_folder(auth_headers):
    parent = client.post("/folders/", json={"name": "Parent"}, headers=auth_headers).json()
    child = client.post("/folders/", json={"name": "Child", "parent_id": parent["id"]}, headers=auth_headers).json()
    assert child["parent_id"] == parent["id"]
