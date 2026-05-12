from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class MessageCreate(BaseModel):
    chat_id: str
    role: Literal["user", "assistant", "system"] = "user"
    content: str


class MessageUpdate(BaseModel):
    content: Optional[str] = None
    role: Optional[Literal["user", "assistant", "system"]] = None


class MessageResponse(BaseModel):
    id: str
    chat_id: str
    user_id: str
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
