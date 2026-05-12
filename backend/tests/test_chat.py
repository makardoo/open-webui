import pytest
from fastapi.testclient import TestClient
from main import app
from backend.apps.chat import store as chat_store
from backend.apps.auth import store as user_store  # adjust if needed

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_data():
    chat_store.clear_all()
    yield
    chat_store.clear_all()


def _register_and_token(email="chat@example.com", password="password123"):
    client.post("/auth/register", json={"email": email, "name": "Chat User", "password": password})
    resp = client.post("/auth/signin", json={"email": email, "password": password})
    return resp.json()["token"]


def auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}


def test_create_chat():
    token = _register_and_token()
    resp = client.post("/chats/", json={"title": "My Chat"}, headers=auth_headers(token))
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "My Chat"
    assert "id" in data


def test_list_chats():
    token = _register_and_token()
    client.post("/chats/", json={"title": "Chat 1"}, headers=auth_headers(token))
    client.post("/chats/", json={"title": "Chat 2"}, headers=auth_headers(token))
    resp = client.get("/chats/", headers=auth_headers(token))
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_chat():
    token = _register_and_token()
    created = client.post("/chats/", json={"title": "Test"}, headers=auth_headers(token)).json()
    resp = client.get(f"/chats/{created['id']}", headers=auth_headers(token))
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_update_chat():
    token = _register_and_token()
    created = client.post("/chats/", json={"title": "Old Title"}, headers=auth_headers(token)).json()
    resp = client.put(f"/chats/{created['id']}", json={"title": "New Title"}, headers=auth_headers(token))
    assert resp.status_code == 200
    assert resp.json()["title"] == "New Title"


def test_delete_chat():
    token = _register_and_token()
    created = client.post("/chats/", json={"title": "To Delete"}, headers=auth_headers(token)).json()
    resp = client.delete(f"/chats/{created['id']}", headers=auth_headers(token))
    assert resp.status_code == 204
    get_resp = client.get(f"/chats/{created['id']}", headers=auth_headers(token))
    assert get_resp.status_code == 404


def test_get_chat_not_found():
    token = _register_and_token()
    resp = client.get("/chats/nonexistent-id", headers=auth_headers(token))
    assert resp.status_code == 404
