import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.apps.prompt.store import _clear_all as clear_prompts
from backend.apps.auth.store import _clear_all as clear_users

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_data():
    clear_users()
    clear_prompts()
    yield
    clear_users()
    clear_prompts()


def _register_and_token(email="prompt@example.com", password="secret123"):
    client.post("/auth/register", json={"email": email, "password": password, "name": "Prompt User"})
    resp = client.post("/auth/signin", json={"email": email, "password": password})
    return resp.json()["access_token"]


@pytest.fixture
def auth_headers():
    token = _register_and_token()
    return {"Authorization": f"Bearer {token}"}


def test_create_prompt(auth_headers):
    resp = client.post(
        "/prompts/",
        json={"title": "My Prompt", "content": "Say hello", "description": "A greeting"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "My Prompt"
    assert data["content"] == "Say hello"


def test_list_prompts(auth_headers):
    client.post("/prompts/", json={"title": "P1", "content": "c1"}, headers=auth_headers)
    client.post("/prompts/", json={"title": "P2", "content": "c2"}, headers=auth_headers)
    resp = client.get("/prompts/", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_prompt(auth_headers):
    created = client.post("/prompts/", json={"title": "T", "content": "C"}, headers=auth_headers).json()
    resp = client.get(f"/prompts/{created['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_update_prompt(auth_headers):
    created = client.post("/prompts/", json={"title": "Old", "content": "old content"}, headers=auth_headers).json()
    resp = client.put(f"/prompts/{created['id']}", json={"title": "New"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "New"
    assert resp.json()["content"] == "old content"


def test_delete_prompt(auth_headers):
    created = client.post("/prompts/", json={"title": "Del", "content": "bye"}, headers=auth_headers).json()
    resp = client.delete(f"/prompts/{created['id']}", headers=auth_headers)
    assert resp.status_code == 200
    resp2 = client.get(f"/prompts/{created['id']}", headers=auth_headers)
    assert resp2.status_code == 404


def test_get_prompt_not_found(auth_headers):
    resp = client.get("/prompts/nonexistent-id", headers=auth_headers)
    assert resp.status_code == 404
