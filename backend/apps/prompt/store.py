from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

_prompts: dict = {}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_prompt(user_id: str, title: str, content: str, description: str = "") -> dict:
    prompt_id = str(uuid4())
    now = _now()
    prompt = {
        "id": prompt_id,
        "user_id": user_id,
        "title": title,
        "content": content,
        "description": description,
        "created_at": now,
        "updated_at": now,
    }
    _prompts[prompt_id] = prompt
    return prompt


def get_prompt(prompt_id: str) -> Optional[dict]:
    return _prompts.get(prompt_id)


def list_prompts_by_user(user_id: str) -> list:
    return [p for p in _prompts.values() if p["user_id"] == user_id]


def update_prompt(prompt_id: str, **kwargs) -> Optional[dict]:
    prompt = _prompts.get(prompt_id)
    if not prompt:
        return None
    for key, value in kwargs.items():
        if key in ("title", "content", "description") and value is not None:
            prompt[key] = value
    prompt["updated_at"] = _now()
    return prompt


def delete_prompt(prompt_id: str) -> bool:
    if prompt_id in _prompts:
        del _prompts[prompt_id]
        return True
    return False


def _clear_all() -> None:
    _prompts.clear()
