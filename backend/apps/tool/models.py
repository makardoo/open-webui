from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime


class ToolCreate(BaseModel):
    name: str
    description: Optional[str] = None
    content: str
    meta: Optional[Dict[str, Any]] = None

    class Config:
        extra = "allow"


class ToolUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

    class Config:
        extra = "allow"


class ToolResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    content: str
    meta: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
