import uuid
from datetime import datetime, timezone
from typing import Optional

from backend.apps.message.models import MessageCreate, MessageUpdate, MessageResponse

_messages: dict[str, dict] = {}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_message(user_id: str, data: MessageCreate) -> MessageResponse:
    msg_id = str(uuid.uuid4())
    now = _now()
    record = {
        "id": msg_id,
        "chat_id": data.chat_id,
        "user_id": user_id,
        "role": data.role,
        "content": data.content,
        "created_at": now,
        "updated_at": now,
    }
    _messages[msg_id] = record
    return MessageResponse(**record)


def get_message(message_id: str) -> Optional[MessageResponse]:
    record = _messages.get(message_id)
    return MessageResponse(**record) if record else None


def list_messages_by_chat(chat_id: str) -> list[MessageResponse]:
    return [
        MessageResponse(**r)
        for r in _messages.values()
        if r["chat_id"] == chat_id
    ]


def update_message(message_id: str, data: MessageUpdate) -> Optional[MessageResponse]:
    record = _messages.get(message_id)
    if not record:
        return None
    if data.content is not None:
        record["content"] = data.content
    if data.role is not None:
        record["role"] = data.role
    record["updated_at"] = _now()
    return MessageResponse(**record)


def delete_message(message_id: str) -> bool:
    if message_id in _messages:
        del _messages[message_id]
        return True
    return False


def clear_all() -> None:
    _messages.clear()
