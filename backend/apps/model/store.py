from datetime import datetime, timezone
from typing import Optional
from tinydb import TinyDB, Query

db = TinyDB("model_store.json")
table = db.table("models")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_model(user_id: str, name: str, base_model: str, system_prompt: Optional[str] = None, params: Optional[dict] = None) -> dict:
    model = {
        "id": f"{user_id}_{name}_{_now()}",
        "user_id": user_id,
        "name": name,
        "base_model": base_model,
        "system_prompt": system_prompt or "",
        "params": params or {},
        "created_at": _now(),
        "updated_at": _now(),
    }
    table.insert(model)
    return model


def get_model(model_id: str) -> Optional[dict]:
    M = Query()
    results = table.search(M.id == model_id)
    return results[0] if results else None


def list_models_by_user(user_id: str) -> list:
    M = Query()
    return table.search(M.user_id == user_id)


def update_model(model_id: str, updates: dict) -> Optional[dict]:
    M = Query()
    updates["updated_at"] = _now()
    table.update(updates, M.id == model_id)
    return get_model(model_id)


def delete_model(model_id: str) -> bool:
    M = Query()
    removed = table.remove(M.id == model_id)
    return len(removed) > 0


def clear_all_models() -> None:
    table.truncate()
