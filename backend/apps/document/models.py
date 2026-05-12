from pydantic import BaseModel
from typing import Optional


class DocumentCreate(BaseModel):
    title: str
    content: str
    collection_name: Optional[str] = None

    class Config:
        extra = "allow"


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    collection_name: Optional[str] = None

    class Config:
        extra = "allow"


class DocumentResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    collection_name: Optional[str] = None
    created_at: int
    updated_at: int

    class Config:
        extra = "allow"
