from pydantic import BaseModel
from typing import Optional


class ModelCreate(BaseModel):
    name: str
    provider: str
    model_id: str
    description: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True


class ModelUpdate(BaseModel):
    name: Optional[str] = None
    provider: Optional[str] = None
    model_id: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True


class ModelResponse(BaseModel):
    id: str
    user_id: str
    name: str
    provider: str
    model_id: str
    description: Optional[str] = None
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
