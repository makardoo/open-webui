from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .models import Token, UserLogin, UserRegister, UserResponse
from .utils import hash_password, verify_password, create_access_token, decode_token
from typing import Optional
import time
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# In-memory store for demo; replace with DB in production
_users: dict = {}


@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister):
    if user_data.email in _users:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "name": user_data.name,
        "email": user_data.email,
        "password": hash_password(user_data.password),
        "role": "user",
        "profile_image_url": "/user.png",
        "created_at": int(time.time()),
    }
    _users[user_data.email] = user
    return UserResponse(**{k: v for k, v in user.items() if k != "password"})


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = _users.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user["id"], "email": user["email"]})
    return Token(access_token=token)


@router.post("/signin", response_model=Token)
def signin(login_data: UserLogin):
    user = _users.get(login_data.email)
    if not user or not verify_password(login_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user["id"], "email": user["email"]})
    return Token(access_token=token)


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_token(token)
    email = payload.get("email")
    user = _users.get(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(**{k: v for k, v in current_user.items() if k != "password"})
