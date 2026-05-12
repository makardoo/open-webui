import pytest
from fastapi.testclient import TestClient

from backend.main import app
import backend.apps.message.store as message_store
import backend.apps.chat.store as chat_store
from backend.apps.auth.store import clear_all as clear_users

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_data():
    clear_users()
    chat_store.clear_all()
    message_store.clear_all()
    yield
    clear_users()
    chat_store.clear_all()
    message_store.clear_all()


def _register_and_token(email="msg@example.com", password="pass1234"):
    client.post("/auth/register", json={"email": email, "password": password, "name": "Tester"})
    resp = client.post("/auth/signin", json={"email": email, "password": password})
    return resp.json()["token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _create_chat(headers):
    resp = client.post("/chats/", json={"title": "Test Chat", "messages": []}, headers=headers)
    return resp.json()["id"]


def test_create_message():
    token = _register_and_token()
    headers = auth_headers(token)
    chat_id = _create_chat(headers)
    resp = client.post("/messages/", json={"chat_id": chat_id, "role": "user", "content": "Hello"}, headers=headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["content"] == "Hello"
    assert data["role"] == "user"
    assert data["chat_id"] == chat_id


def test_list_messages_by_chat():
    token = _register_and_token()
    headers = auth_headers(token)
    chat_id = _create_chat(headers)
    client.post("/messages/", json={"chat_id": chat_id, "role": "user", "content": "Msg 1"}, headers=headers)
    client.post("/messages/", json={"chat_id": chat_id, "role": "assistant", "content": "Msg 2"}, headers=headers)
    resp = client.get(f"/messages/chat/{chat_id}", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_message():
    token = _register_and_token()
    headers = auth_headers(token)
    chat_id = _create_chat(headers)
    created = client.post("/messages/", json={"chat_id": chat_id, "role": "user", "content": "Hi"}, headers=headers).json()
    resp = client.get(f"/messages/{created['id']}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_update_message():
    token = _register_and_token()
    headers = auth_headers(token)
    chat_id = _create_chat(headers)
    created = client.post("/messages/", json={"chat_id": chat_id, "role": "user", "content": "Old"}, headers=headers).json()
    resp = client.patch(f"/messages/{created['id']}", json={"content": "New"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["content"] == "New"


def test_delete_message():
    token = _register_and_token()
    headers = auth_headers(token)
    chat_id = _create_chat(headers)
    created = client.post("/messages/", json={"chat_id": chat_id, "role": "user", "content": "Bye"}, headers=headers).json()
    resp = client.delete(f"/messages/{created['id']}", headers=headers)
    assert resp.status_code == 204
    resp2 = client.get(f"/messages/{created['id']}", headers=headers)
    assert resp2.status_code == 404
