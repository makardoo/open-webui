from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from backend.apps.auth.router import get_current_user
from backend.apps.auth.models import UserResponse
from backend.apps.chat.models import ChatCreate, ChatUpdate, ChatResponse
from backend.apps.chat import store

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat(
    payload: ChatCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    return store.create_chat(user_id=current_user.id, payload=payload)


@router.get("/", response_model=List[ChatResponse])
def list_chats(
    current_user: UserResponse = Depends(get_current_user),
):
    return store.list_chats(user_id=current_user.id)


@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(
    chat_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    chat = store.get_chat(chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return chat


@router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(
    chat_id: str,
    payload: ChatUpdate,
    current_user: UserResponse = Depends(get_current_user),
):
    chat = store.update_chat(chat_id=chat_id, user_id=current_user.id, payload=payload)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return chat


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(
    chat_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    deleted = store.delete_chat(chat_id=chat_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
