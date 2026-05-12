from pydantic import BaseModel
from typing import Optional
import time


class FolderCreate(BaseModel):
    name: str
    parent_id: Optional[str] = None


class FolderUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[str] = None


class FolderResponse(BaseModel):
    id: str
    user_id: str
    name: str
    parent_id: Optional[str] = None
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True
