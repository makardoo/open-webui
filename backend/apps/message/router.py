from fastapi import APIRouter, Depends, HTTPException, status

from backend.apps.auth.router import get_current_user
from backend.apps.auth.models import UserResponse
from backend.apps.message.models import MessageCreate, MessageUpdate, MessageResponse
import backend.apps.message.store as store

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_message(
    data: MessageCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    return store.create_message(user_id=current_user.id, data=data)


@router.get("/chat/{chat_id}", response_model=list[MessageResponse])
def list_messages(
    chat_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    return store.list_messages_by_chat(chat_id=chat_id)


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(
    message_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    msg = store.get_message(message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg


@router.patch("/{message_id}", response_model=MessageResponse)
def update_message(
    message_id: str,
    data: MessageUpdate,
    current_user: UserResponse = Depends(get_current_user),
):
    msg = store.update_message(message_id, data)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(
    message_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    deleted = store.delete_message(message_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Message not found")
