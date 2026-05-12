from pydantic import BaseModel
from typing import Optional


class PromptCreate(BaseModel):
    title: str
    content: str
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Summarize",
                "content": "Summarize the following text in 3 bullet points:",
                "description": "A prompt to summarize text",
            }
        }


class PromptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Summarize v2",
                "content": "Summarize the following text concisely:",
            }
        }


class PromptResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    description: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
