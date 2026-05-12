import uuid
from datetime import datetime, timezone
from typing import List, Optional

from apps.prompt.models import PromptCreate, PromptUpdate, PromptResponse

_prompts: dict[str, dict] = {}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_prompt(user_id: str, data: PromptCreate) -> PromptResponse:
    prompt_id = str(uuid.uuid4())
    now = _now()
    record = {
        "id": prompt_id,
        "user_id": user_id,
        "title": data.title,
        "content": data.content,
        "description": data.description,
        "created_at": now,
        "updated_at": now,
    }
    _prompts[prompt_id] = record
    return PromptResponse(**record)


def get_prompt(prompt_id: str) -> Optional[PromptResponse]:
    record = _prompts.get(prompt_id)
    if record is None:
        return None
    return PromptResponse(**record)


def list_prompts_by_user(user_id: str) -> List[PromptResponse]:
    return [
        PromptResponse(**r)
        for r in _prompts.values()
        if r["user_id"] == user_id
    ]


def update_prompt(prompt_id: str, data: PromptUpdate) -> Optional[PromptResponse]:
    record = _prompts.get(prompt_id)
    if record is None:
        return None
    updates = data.model_dump(exclude_none=True)
    record.update(updates)
    record["updated_at"] = _now()
    _prompts[prompt_id] = record
    return PromptResponse(**record)


def delete_prompt(prompt_id: str) -> bool:
    if prompt_id not in _prompts:
        return False
    del _prompts[prompt_id]
    return True
