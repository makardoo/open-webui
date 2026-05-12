import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from backend.apps.auth.router import router, _users
from backend.apps.auth.utils import hash_password, verify_password, create_access_token, decode_token

app = FastAPI()
app.include_router(router)
client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_users():
    _users.clear()
    yield
    _users.clear()


def test_register_user():
    response = client.post("/auth/register", json={
        "name": "Test User", "email": "test@example.com", "password": "secret123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["role"] == "user"
    assert "password" not in data


def test_register_duplicate_email():
    client.post("/auth/register", json={
        "name": "Test User", "email": "test@example.com", "password": "secret123"
    })
    response = client.post("/auth/register", json={
        "name": "Another", "email": "test@example.com", "password": "other"
    })
    assert response.status_code == 400


def test_signin():
    client.post("/auth/register", json={
        "name": "Test User", "email": "test@example.com", "password": "secret123"
    })
    response = client.post("/auth/signin", json={"email": "test@example.com", "password": "secret123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_signin_invalid_credentials():
    response = client.post("/auth/signin", json={"email": "no@one.com", "password": "wrong"})
    assert response.status_code == 401


def test_get_me():
    client.post("/auth/register", json={
        "name": "Test User", "email": "test@example.com", "password": "secret123"
    })
    token_resp = client.post("/auth/signin", json={"email": "test@example.com", "password": "secret123"})
    token = token_resp.json()["access_token"]
    me_resp = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "test@example.com"


def test_password_hashing():
    hashed = hash_password("mypassword")
    assert verify_password("mypassword", hashed)
    assert not verify_password("wrongpassword", hashed)


def test_token_encode_decode():
    token = create_access_token({"sub": "user-id", "email": "a@b.com"})
    payload = decode_token(token)
    assert payload["email"] == "a@b.com"
