import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from backend.apps.chat.models import ChatCreate, ChatUpdate, ChatResponse, MessageBase

# In-memory store; replace with DB integration as needed
_chats: Dict[str, dict] = {}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_chat(user_id: str, payload: ChatCreate) -> ChatResponse:
    chat_id = str(uuid.uuid4())
    now = _now()
    chat = {
        "id": chat_id,
        "user_id": user_id,
        "title": payload.title or "New Chat",
        "messages": [m.dict() for m in (payload.messages or [])],
        "created_at": now,
        "updated_at": now,
    }
    _chats[chat_id] = chat
    return ChatResponse(**chat)


def get_chat(chat_id: str, user_id: str) -> Optional[ChatResponse]:
    chat = _chats.get(chat_id)
    if chat and chat["user_id"] == user_id:
        return ChatResponse(**chat)
    return None


def list_chats(user_id: str) -> List[ChatResponse]:
    return [
        ChatResponse(**c) for c in _chats.values() if c["user_id"] == user_id
    ]


def update_chat(chat_id: str, user_id: str, payload: ChatUpdate) -> Optional[ChatResponse]:
    chat = _chats.get(chat_id)
    if not chat or chat["user_id"] != user_id:
        return None
    if payload.title is not None:
        chat["title"] = payload.title
    if payload.messages is not None:
        chat["messages"] = [m.dict() for m in payload.messages]
    chat["updated_at"] = _now()
    _chats[chat_id] = chat
    return ChatResponse(**chat)


def delete_chat(chat_id: str, user_id: str) -> bool:
    chat = _chats.get(chat_id)
    if chat and chat["user_id"] == user_id:
        del _chats[chat_id]
        return True
    return False


def clear_all() -> None:
    _chats.clear()
