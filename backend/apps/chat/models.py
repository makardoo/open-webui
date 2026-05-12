from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MessageBase(BaseModel):
    role: str
    content: str


class ChatMessage(MessageBase):
    id: str
    chat_id: str
    user_id: str
    timestamp: datetime

    class Config:
        from_attributes = True


class ChatCreate(BaseModel):
    title: Optional[str] = "New Chat"
    messages: Optional[List[MessageBase]] = []


class ChatUpdate(BaseModel):
    title: Optional[str] = None
    messages: Optional[List[MessageBase]] = None


class ChatResponse(BaseModel):
    id: str
    user_id: str
    title: str
    messages: List[MessageBase]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
