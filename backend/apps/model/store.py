from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

_store: dict[str, dict] = {}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_model(user_id: str, data: dict) -> dict:
    model_id = str(uuid4())
    now = _now()
    record = {
        "id": model_id,
        "user_id": user_id,
        "name": data["name"],
        "provider": data["provider"],
        "model_id": data["model_id"],
        "description": data.get("description"),
        "is_active": data.get("is_active", True),
        "created_at": now,
        "updated_at": now,
    }
    _store[model_id] = record
    return record


def get_model(model_id: str) -> Optional[dict]:
    return _store.get(model_id)


def list_models_by_user(user_id: str) -> list[dict]:
    return [m for m in _store.values() if m["user_id"] == user_id]


def update_model(model_id: str, data: dict) -> Optional[dict]:
    record = _store.get(model_id)
    if not record:
        return None
    for key, value in data.items():
        if value is not None:
            record[key] = value
    record["updated_at"] = _now()
    return record


def delete_model(model_id: str) -> bool:
    if model_id in _store:
        del _store[model_id]
        return True
    return False
