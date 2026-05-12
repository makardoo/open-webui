import pytest
from fastapi.testclient import TestClient
from main import app
from apps.document import store as doc_store
from apps.auth import store as auth_store

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_data():
    doc_store._documents.clear()
    auth_store._users.clear()
    yield
    doc_store._documents.clear()
    auth_store._users.clear()


def _register_and_token(email="doc@example.com", password="secret"):
    client.post("/auth/register", json={"email": email, "password": password, "name": "Doc User"})
    resp = client.post("/auth/signin", json={"email": email, "password": password})
    return resp.json()["token"]


@pytest.fixture
def auth_headers():
    token = _register_and_token()
    return {"Authorization": f"Bearer {token}"}


def test_create_document(auth_headers):
    resp = client.post("/documents/", json={"title": "Doc 1", "content": "Hello world"}, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Doc 1"
    assert data["content"] == "Hello world"
    assert "id" in data


def test_list_documents(auth_headers):
    client.post("/documents/", json={"title": "A", "content": "aaa"}, headers=auth_headers)
    client.post("/documents/", json={"title": "B", "content": "bbb"}, headers=auth_headers)
    resp = client.get("/documents/", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_document(auth_headers):
    created = client.post("/documents/", json={"title": "Get Me", "content": "content"}, headers=auth_headers).json()
    resp = client.get(f"/documents/{created['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Get Me"


def test_update_document(auth_headers):
    created = client.post("/documents/", json={"title": "Old", "content": "old content"}, headers=auth_headers).json()
    resp = client.put(f"/documents/{created['id']}", json={"title": "New"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "New"
    assert resp.json()["content"] == "old content"


def test_delete_document(auth_headers):
    created = client.post("/documents/", json={"title": "Del", "content": "bye"}, headers=auth_headers).json()
    resp = client.delete(f"/documents/{created['id']}", headers=auth_headers)
    assert resp.status_code == 204
    resp2 = client.get(f"/documents/{created['id']}", headers=auth_headers)
    assert resp2.status_code == 404


def test_get_document_not_found(auth_headers):
    resp = client.get("/documents/nonexistent", headers=auth_headers)
    assert resp.status_code == 404
