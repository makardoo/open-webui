from pydantic import BaseModel
from typing import Optional


class TagCreate(BaseModel):
    name: str
    color: Optional[str] = None

    class Config:
        str_strip_whitespace = True


class TagUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None

    class Config:
        str_strip_whitespace = True


class TagResponse(BaseModel):
    id: str
    user_id: str
    name: str
    color: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
